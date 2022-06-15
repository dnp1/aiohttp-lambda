from aiohttp import HttpVersion
from aiohttp.http_parser import RawRequestMessage
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL

from .lambda_request_type import AwsLambdaRequest


def build_message(event: AwsLambdaRequest) -> RawRequestMessage:
    context = event['requestContext']
    http = context['http']
    version = http['protocol'].lstrip('HTTP/').split('.')
    http_version = HttpVersion(int(version[0]), int(version[1]))
    url = URL.build(scheme='http',
                    host=context['domainName'],
                    path=http['path'],
                    query_string=event['rawQueryString'])
    headers_ = CIMultiDict(event['headers'])

    return RawRequestMessage(
        method=http['method'].upper(),
        path=http['path'],
        version=http_version,
        headers=CIMultiDictProxy(headers_),
        raw_headers=tuple((k.encode(), v.encode()) for k, v in event['headers'].items()),
        should_close=False,
        compression=None,
        upgrade=False,
        chunked=False,
        url=url,
    )
