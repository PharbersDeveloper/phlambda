import json
import os

from parse_event import Parse
from git_python import GitRepository
from package_code import zip_code, start_codebuild

def lambda_handler(event, context):
    # 测试cicd1548
    parse = Parse()
    print(event)

    git_event = parse.print_branch_information(event=event)
    print(git_event)
    if git_event['operator_name'] == "hbzhao" and git_event.get("event_type") == "MERGED":
        os.getenv("GIT_URL")
        git_url = 'https://hbzhao:123456@bitbucket.pharbers.com/scm/lgc/phlambda.git'
        local_path_prefix = '/tmp'
        local_path = os.path.join(local_path_prefix, 'phlambda')
        # 从bitbucket下载代码 存放在local_path下
        repo = GitRepository(local_path, git_url, branch='PBDP-1871-lambda-directory-code-build')

        # 打包上传代码
        # 获取git commit 版版本
        git_commit_version = git_event["git_commit_version"]
        zip_code(local_path, git_commit_version)

        # 启动所有项目的codebuild
        start_codebuild()

        return {
            "statusCode": 200,
            "body": json.dumps("CICD Complete")
        }

    return {
        "statusCode": 200,
        "body": json.dumps("The git operation type must be merge")
    }

if __name__ == '__main__':
    event = {'resource': '/integration', 'path': '/integration', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Content-Type': 'application/json; charset=UTF-8', 'Host': '2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn', 'User-Agent': 'Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default', 'Via': '1.1 localhost (Apache-HttpClient/4.5.5 (cache))', 'X-Amzn-Trace-Id': 'Root=1-614d39d7-4cb354047e261f8d148dc453', 'X-Event-Key': 'pr:merged', 'X-Forwarded-For': '52.82.70.180', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https', 'X-Request-Id': '146bb84a-c3ee-4bdc-8d5a-7db8817d04a5'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Content-Type': ['application/json; charset=UTF-8'], 'Host': ['2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn'], 'User-Agent': ['Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default'], 'Via': ['1.1 localhost (Apache-HttpClient/4.5.5 (cache))'], 'X-Amzn-Trace-Id': ['Root=1-614d39d7-4cb354047e261f8d148dc453'], 'X-Event-Key': ['pr:merged'], 'X-Forwarded-For': ['52.82.70.180'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https'], 'X-Request-Id': ['146bb84a-c3ee-4bdc-8d5a-7db8817d04a5']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'gqk3k1', 'resourcePath': '/integration', 'httpMethod': 'POST', 'extendedRequestId': 'GJX5oGKRZPgF91Q=', 'requestTime': '24/Sep/2021:02:37:11 +0000', 'path': '/v0/integration', 'accountId': '444603803904', 'protocol': 'HTTP/1.1', 'stage': 'v0', 'domainPrefix': '2t69b7x032', 'requestTimeEpoch': 1632451031044, 'requestId': '7032c0ba-890f-4959-85be-b5af408a1f62', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '52.82.70.180', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Atlassian HttpClient 2.0.0 / Bitbucket-6.5.2 (6005002) / Default', 'user': None}, 'domainName': '2t69b7x032.execute-api.cn-northwest-1.amazonaws.com.cn', 'apiId': '2t69b7x032'}, 'body': '{"eventKey":"pr:merged","date":"2021-09-24T10:37:10+0800","actor":{"name":"hbzhao","emailAddress":"hbzhao@data-pharbers.com","id":302,"displayName":"赵浩博","active":true,"slug":"hbzhao","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/users/hbzhao"}]}},"pullRequest":{"id":84,"version":2,"title":"Feature/PBDP-1942 clickhouse sql","description":"* 修改打包代码防止打包错误\\r\\n* 测试打包多个lmd 触发codebuild","state":"MERGED","open":false,"closed":true,"createdDate":1632450964000,"updatedDate":1632451031000,"closedDate":1632451031000,"fromRef":{"id":"refs/heads/feature/PBDP-1942-clickhouse-sql","displayId":"feature/PBDP-1942-clickhouse-sql","latestCommit":"7a49befd35a164f5a14b1ef8430f8cb0bd443150","repository":{"slug":"phlambda","id":13,"name":"phlambda","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":true,"project":{"key":"LGC","id":25,"name":"logic","description":"业务逻辑层","public":false,"type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC"}]}},"public":false,"links":{"clone":[{"href":"https://bitbucket.pharbers.com/scm/lgc/phlambda.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/lgc/phlambda.git","name":"ssh"}],"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC/repos/phlambda/browse"}]}}},"toRef":{"id":"refs/heads/PBDP-1871-lambda-directory-code-build","displayId":"PBDP-1871-lambda-directory-code-build","latestCommit":"eff46e46dcd1bd62f95c91dc19d527d00281f6fe","repository":{"slug":"phlambda","id":13,"name":"phlambda","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":true,"project":{"key":"LGC","id":25,"name":"logic","description":"业务逻辑层","public":false,"type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC"}]}},"public":false,"links":{"clone":[{"href":"https://bitbucket.pharbers.com/scm/lgc/phlambda.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/lgc/phlambda.git","name":"ssh"}],"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC/repos/phlambda/browse"}]}}},"locked":false,"author":{"user":{"name":"hbzhao","emailAddress":"hbzhao@data-pharbers.com","id":302,"displayName":"赵浩博","active":true,"slug":"hbzhao","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/users/hbzhao"}]}},"role":"AUTHOR","approved":false,"status":"UNAPPROVED"},"reviewers":[],"participants":[],"properties":{"mergeCommit":{"displayId":"6814732cc39","id":"6814732cc3946475fe7db164b4e3e50d6b021c15"}},"links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC/repos/phlambda/pull-requests/84"}]}}}', 'isBase64Encoded': False}

    lambda_handler(event=event, context=None)
