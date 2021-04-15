import json
from src.parse_event import Parse

def lambda_handler(event, context):

    parse = Parse()
    print(parse.print_branch_information(event=event))
    return {
        "statusCode": 200,
        "body": json.dumps("Hello from Lambda")
    }

if __name__ == "__main__":
    merge_event = {"resource": "/integration", "path": "/integration", "httpMethod": "POST",
                   "headers": {"Accept": "*/*", "Content-Type": "application/json; charset=UTF-8",
                               "Host": "2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn",
                               "User-Agent": "Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default",
                               "Via": "1.1 localhost (Apache-HttpClient/4.5.5 (cache))",
                               "X-Amzn-Trace-Id": "Root=1-606feb86-2ca668c86e8b65e168bea0bd",
                               "X-Event-Key": "pr:merged",
                               "X-Forwarded-For": "161.189.223.39", "X-Forwarded-Port": "443",
                               "X-Forwarded-Proto": "https",
                               "X-Request-Id": "8445727e-ddda-4fbd-97f0-7165ac33078e"},
                   "multiValueHeaders": {"Accept": ["*/*"], "Content-Type": ["application/json; charset=UTF-8"],
                                         "Host": ["2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn"],
                                         "User-Agent": [
                                             "Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default"],
                                         "Via": ["1.1 localhost (Apache-HttpClient/4.5.5 (cache))"],
                                         "X-Amzn-Trace-Id": ["Root=1-606feb86-2ca668c86e8b65e168bea0bd"],
                                         "X-Event-Key": ["pr:merged"], "X-Forwarded-For": ["161.189.223.39"],
                                         "X-Forwarded-Port": ["443"], "X-Forwarded-Proto": ["https"],
                                         "X-Request-Id": ["8445727e-ddda-4fbd-97f0-7165ac33078e"]},
                   "queryStringParameters": None, "multiValueQueryStringParameters": None, "pathParameters": None,
                   "stageVariables": None,
                   "requestContext": {"resourceId": "gqk3k1", "resourcePath": "/integration", "httpMethod": "POST",
                                      "extendedRequestId": "dgG9AFw-5PgF8mw=",
                                      "requestTime": "09/Apr/2021:05:52:06 +0000",
                                      "path": "/v0/integration", "accountId": "444603803904", "protocol": "HTTP/1.1",
                                      "stage": "v0", "domainPrefix": "2t69b7x032", "requestTimeEpoch": 1617947526397,
                                      "requestId": "b4ea7751-fe3e-4629-a300-2b55afbcf63d",
                                      "identity": {"cognitoIdentityPoolId": None, "accountId": None,
                                                   "cognitoIdentityId": None, "caller": None,
                                                   "sourceIp": "161.189.223.39",
                                                   "principalOrgId": None, "accessKey": None,
                                                   "cognitoAuthenticationType": None,
                                                   "cognitoAuthenticationProvider": None,
                                                   "userArn": None,
                                                   "userAgent": "Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default",
                                                   "user": None},
                                      "domainName": "2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn",
                                      "apiId": "2t69b7x032"},
                   'body': '{"eventKey":"pr:merged","date":"2021-04-09T13:52:06+0800","actor":{"name":"Alfred","emailAddress":"alfredyang@pharbers.com","id":70,"displayName":"杨渊","active":true,"slug":"alfred","type":"NORMAL","links":{"self":[{"href":"http://bitbucket.pharbers.com/users/alfred"}]}},"pullRequest":{"id":1,"version":2,"title":"merge test","description":"测试merge时发送的event","state":"MERGED","open":false,"closed":true,"createdDate":1617947474000,"updatedDate":1617947526000,"closedDate":1617947526000,"fromRef":{"id":"refs/heads/test_merge","displayId":"test_merge","latestCommit":"9255cfaf5a25e24e84eed1c923040cbc5c1c6883","repository":{"slug":"cicdinittest","id":68,"name":"cicdinittest","description":"cicdinittest","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":true,"project":{"key":"TMIS","id":107,"name":"tmist","description":"专供铁马","public":false,"type":"NORMAL","links":{"self":[{"href":"http://bitbucket.pharbers.com/projects/TMIS"}]}},"public":false,"links":{"clone":[{"href":"http://bitbucket.pharbers.com/scm/tmis/cicdinittest.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/tmis/cicdinittest.git","name":"ssh"}],"self":[{"href":"http://bitbucket.pharbers.com/projects/TMIS/repos/cicdinittest/browse"}]}}},"toRef":{"id":"refs/heads/master","displayId":"master","latestCommit":"0414829e6f37a4a670b8448dfca07b1301285f33","repository":{"slug":"cicdinittest","id":68,"name":"cicdinittest","description":"cicdinittest","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":true,"project":{"key":"TMIS","id":107,"name":"tmist","description":"专供铁马","public":false,"type":"NORMAL","links":{"self":[{"href":"http://bitbucket.pharbers.com/projects/TMIS"}]}},"public":false,"links":{"clone":[{"href":"http://bitbucket.pharbers.com/scm/tmis/cicdinittest.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/tmis/cicdinittest.git","name":"ssh"}],"self":[{"href":"http://bitbucket.pharbers.com/projects/TMIS/repos/cicdinittest/browse"}]}}},"locked":false,"author":{"user":{"name":"hbzhao","emailAddress":"hbzhao@data-pharbers.com","id":302,"displayName":"hbzhao","active":true,"slug":"hbzhao","type":"NORMAL","links":{"self":[{"href":"http://bitbucket.pharbers.com/users/hbzhao"}]}},"role":"AUTHOR","approved":false,"status":"UNAPPROVED"},"reviewers":[{"user":{"name":"Alfred","emailAddress":"alfredyang@pharbers.com","id":70,"displayName":"杨渊","active":true,"slug":"alfred","type":"NORMAL","links":{"self":[{"href":"http://bitbucket.pharbers.com/users/alfred"}]}},"lastReviewedCommit":"9255cfaf5a25e24e84eed1c923040cbc5c1c6883","role":"REVIEWER","approved":true,"status":"APPROVED"}],"participants":[],"properties":{"mergeCommit":{"displayId":"daac12427c8","id":"daac12427c8a438be5d6ede78d1b95f3483d6212"}},"links":{"self":[{"href":"http://bitbucket.pharbers.com/projects/TMIS/repos/cicdinittest/pull-requests/1"}]}}}',
                   "isBase64Encoded": False}
    add_event = {"resource": "/integration", "path": "/integration", "httpMethod": "POST",
                 "headers": {"Accept": "*/*", "Content-Type": "application/json; charset=UTF-8",
                             "Host": "2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn",
                             "User-Agent": "Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default",
                             "Via": "1.1 localhost (Apache-HttpClient/4.5.5 (cache))",
                             "X-Amzn-Trace-Id": "Root=1-606ea424-565f3b124d2d0d652b5ce959",
                             "X-Event-Key": "repo:refs_changed", "X-Forwarded-For": "161.189.223.39",
                             "X-Forwarded-Port": "443", "X-Forwarded-Proto": "https",
                             "X-Request-Id": "2440d3d7-8290-4f71-bb43-50d82240957d"},
                 "multiValueHeaders": {"Accept": ["*/*"], "Content-Type": ["application/json; charset=UTF-8"],
                                       "Host": ["2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn"],
                                       "User-Agent": [
                                           "Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default"],
                                       "Via": ["1.1 localhost (Apache-HttpClient/4.5.5 (cache))"],
                                       "X-Amzn-Trace-Id": ["Root=1-606ea424-565f3b124d2d0d652b5ce959"],
                                       "X-Event-Key": ["repo:refs_changed"], "X-Forwarded-For": ["161.189.223.39"],
                                       "X-Forwarded-Port": ["443"], "X-Forwarded-Proto": ["https"],
                                       "X-Request-Id": ["2440d3d7-8290-4f71-bb43-50d82240957d"]},
                 "queryStringParameters": None, "multiValueQueryStringParameters": None, "pathParameters": None,
                 "stageVariables": None,
                 "requestContext": {"resourceId": "gqk3k1", "resourcePath": "/integration", "httpMethod": "POST",
                                    "extendedRequestId": "dc6VsGeB5PgFsDg=",
                                    "requestTime": "08/Apr/2021:06:35:16 +0000",
                                    "path": "/v0/integration", "accountId": "444603803904", "protocol": "HTTP/1.1",
                                    "stage": "v0", "domainPrefix": "2t69b7x032", "requestTimeEpoch": 1617863716344,
                                    "requestId": "510d8c56-cfff-4b2c-bea7-65d8390d1775",
                                    "identity": {"cognitoIdentityPoolId": None, "accountId": None,
                                                 "cognitoIdentityId": None, "caller": None,
                                                 "sourceIp": "161.189.223.39",
                                                 "principalOrgId": None, "accessKey": None,
                                                 "cognitoAuthenticationType": None,
                                                 "cognitoAuthenticationProvider": None,
                                                 "userArn": None,
                                                 "userAgent": "Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default",
                                                 "user": None},
                                    "domainName": "2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn",
                                    "apiId": "2t69b7x032"},
                 'body': '{"eventKey":"repo:refs_changed","date":"2021-04-08T14:35:16+0800","actor":{"name":"hbzhao","emailAddress":"hbzhao@data-pharbers.com","id":302,"displayName":"hbzhao","active":true,"slug":"hbzhao","type":"NORMAL","links":{"self":[{"href":"http://bitbucket.pharbers.com/users/hbzhao"}]}},"repository":{"slug":"cicdinittest","id":68,"name":"cicdinittest","description":"cicdinittest","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":true,"project":{"key":"TMIS","id":107,"name":"tmist","description":"专供铁马","public":false,"type":"NORMAL","links":{"self":[{"href":"http://bitbucket.pharbers.com/projects/TMIS"}]}},"public":false,"links":{"clone":[{"href":"http://bitbucket.pharbers.com/scm/tmis/cicdinittest.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/tmis/cicdinittest.git","name":"ssh"}],"self":[{"href":"http://bitbucket.pharbers.com/projects/TMIS/repos/cicdinittest/browse"}]}},"changes":[{"ref":{"id":"refs/heads/test_merge","displayId":"test_merge","type":"BRANCH"},"refId":"refs/heads/test_merge","fromHash":"0000000000000000000000000000000000000000","toHash":"0414829e6f37a4a670b8448dfca07b1301285f33","type":"ADD"}]}',

                 "isBase64Encoded": False}

    lambda_handler(event=merge_event, context=None)
