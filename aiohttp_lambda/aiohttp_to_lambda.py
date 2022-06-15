from aiohttp import Payload, web
from aiohttp.abc import StreamResponse

from .lambda_response_type import AwsHttpResponse


def convert_aiohttp_response_to_aws_response(resp: StreamResponse) -> AwsHttpResponse:
    if isinstance(resp, web.Response):
        body_ = resp.body
        if isinstance(body_, bytes):
            body = body_.decode()
        elif isinstance(body_, Payload):
            raise NotImplemented
        else:
            body = ''
    else:
        raise NotImplemented

    return {
        'statusCode': resp.status,
        'headers': {k: v for k, v in resp.headers.items()},
        'body': body,
        'cookies': list(resp.cookies),
        'isBase64Encoded': False
    }
