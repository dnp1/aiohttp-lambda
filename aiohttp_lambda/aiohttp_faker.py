import asyncio
from typing import Any

from aiohttp.web_protocol import RequestHandler


class FakeTransport(asyncio.Transport):
    _EXTRA_INFO = {
        'sslcontext': False,
        'peername': 'localhost',
    }

    def get_extra_info(self, key: Any, default: Any = None) -> Any:
        return self._EXTRA_INFO.get(key)


class _RequestHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transport = FakeTransport()
