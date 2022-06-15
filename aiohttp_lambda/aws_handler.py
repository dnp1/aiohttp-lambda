import asyncio
import atexit
import signal
import sys
from asyncio import AbstractEventLoop
from functools import lru_cache
from typing import Any, Optional

from aiohttp import web, StreamReader
from aiohttp.http_writer import StreamWriter
from aiohttp.web_exceptions import HTTPClientError

from .aiohttp_faker import _RequestHandler
from .aiohttp_to_lambda import convert_aiohttp_response_to_aws_response
from .aws_to_aiohttp import build_message
from .lambda_request_type import AwsLambdaRequest
from .lambda_response_type import AwsHttpResponse

KB = 1 << 10
MB = KB << 10


class LambdaHandler:
    def __init__(self, app: web.Application,
                 *,
                 loop: Optional[AbstractEventLoop] = None,
                 input_body_limit: int = 6 * MB - 4 * KB
                 ):
        """

        :param app:
        :param input_body_limit: it limits the incoming body length
        """
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        self._input_body_limit = input_body_limit
        self._app = app
        # noinspection PyProtectedMember
        self._make_request = app._make_request
        # noinspection PyProtectedMember
        self._server = app._make_handler(loop=self._loop)
        # noinspection PyProtectedMember
        self._handle_request = app._handle
        self._handler = _RequestHandler(loop=self._loop, manager=self._server)

    @lru_cache
    def setup_graceful_start_and_stop(self):
        app = self._app
        loop = self._loop
        # noinspection PyProtectedMember
        app._set_loop(loop)
        # noinspection PyProtectedMember
        app._on_startup.freeze()
        # noinspection PyProtectedMember
        app._on_shutdown.freeze()
        loop.run_until_complete(app.startup())

        async def async_shutdown() -> None:
            await app.cleanup()
            await app.shutdown()

        def shutdown():
            loop.run_until_complete(async_shutdown())

        def exit_gracefully(_: Any, __: Any) -> None:
            shutdown()
            sys.exit(0)

        signal.signal(signal.SIGTERM, exit_gracefully)
        atexit.register(shutdown)

    def _lambda_request_to_aiohttp_request(self, event: AwsLambdaRequest) -> web.Request:
        reader = StreamReader(protocol=self._handler, limit=self._input_body_limit)
        if body := event.get('body'):
            reader.feed_data(data=body.encode())
        writer = StreamWriter(self._handler, self._loop)

        # noinspection PyTypeChecker
        request = self._make_request(
            message=build_message(event),
            payload=reader,
            protocol=self._handler,
            writer=writer,
            task=None,  # type: ignore
        )
        return request

    async def _handle_and_convert(self, req: web.Request) -> AwsHttpResponse:
        try:
            resp = await self._server.request_handler(req)
        except HTTPClientError as e:
            resp = e
        return convert_aiohttp_response_to_aws_response(resp)

    def handle(self, event: AwsLambdaRequest, _: Any) -> AwsHttpResponse:
        """
        :param event:
        :param _:
        :return:
        """
        request = self._lambda_request_to_aiohttp_request(event)
        return self._loop.run_until_complete(self._handle_and_convert(request))

    def __call__(self, event: AwsLambdaRequest, context: Any) -> AwsHttpResponse:
        return self.handle(event, context)
