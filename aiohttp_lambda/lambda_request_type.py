from typing import TypedDict, Optional


class AwsIAMAuthorizer(TypedDict):
    accessKey: str
    accountId: str
    callerId: str
    cognitoIdentity: Optional[str]
    principalOrgId: Optional[str]
    userArn: str
    userId: str


class AwsAuthorizer(TypedDict):
    iam: AwsIAMAuthorizer


class AwsHTTPContext(TypedDict):
    method: str
    path: str
    protocol: str
    sourceIp: str
    userAgent: str


class AwsRequestContext(TypedDict):
    accountId: str
    apiId: str
    authentication: Optional[str]
    authorizer: AwsAuthorizer
    domainName: str
    domainPrefix: str
    http: AwsHTTPContext
    requestId: str
    routeKey: str
    stage: str
    time: str
    timeEpoch: int


class AwsLambdaRequest(TypedDict):
    version: str
    routeKey: str
    rawPath: str
    rawQueryString: str
    cookies: list[str]
    headers: dict[str, str]
    queryStringParameters: dict[str, str]
    requestContext: AwsRequestContext
    body: Optional[str]
    pathParameters: Optional[str]
    isBase64Encoded: bool
    stageVariables: Optional[str]
