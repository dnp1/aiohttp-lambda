from .lambda_request_type import AwsLambdaRequest
from .lambda_response_type import AwsHttpResponse

aws_request: AwsLambdaRequest = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/health",
    "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
    "cookies": [
        "cookie1",
        "cookie2"
    ],
    "headers": {
        "header1": "value1",
        "header2": "value1,value2"
    },
    "queryStringParameters": {
        "parameter1": "value1,value2",
        "parameter2": "value"
    },
    "requestContext": {
        "accountId": "123456789012",
        "apiId": "<urlid>",
        "authentication": None,
        "authorizer": {
            "iam": {
                "accessKey": "AKIA...",
                "accountId": "111122223333",
                "callerId": "AIDA...",
                "cognitoIdentity": None,
                "principalOrgId": None,
                "userArn": "arn:aws:iam::111122223333:user/example-user",
                "userId": "AIDA..."
            }
        },
        "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
        "domainPrefix": "<url-id>",
        "http": {
            "method": "GET",
            "path": "/health",
            "protocol": "HTTP/1.1",
            "sourceIp": "123.123.123.123",
            "userAgent": "agent"
        },
        "requestId": "id",
        "routeKey": "$default",
        "stage": "$default",
        "time": "12/Mar/2020:19:03:58 +0000",
        "timeEpoch": 1583348638390
    },
    "body": "Hello from client!",
    "pathParameters": None,
    "isBase64Encoded": False,
    "stageVariables": None
}

aws_response: AwsHttpResponse = {
    "statusCode": 201,
    "headers": {
        "Content-Type": "application/json",
        "My-Custom-Header": "Custom Value"
    },
    "body": "{ \"message\": \"Hello, world!\" }",
    "cookies": [
        "Cookie_1=Value1; Expires=21 Oct 2021 07:48 GMT",
        "Cookie_2=Value2; Max-Age=78000"
    ],
    "isBase64Encoded": False
}
