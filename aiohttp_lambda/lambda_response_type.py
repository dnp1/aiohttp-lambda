from typing import TypedDict, Optional


class AwsHttpResponse(TypedDict):
    statusCode: int
    headers: dict[str, str]
    body: Optional[str]
    cookies: list[str]
    isBase64Encoded: bool
