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
    if git_event['operator_name'] == "hbzhao":
        git_url = 'https://hbzhao:123456@bitbucket.pharbers.com/scm/lgc/phlambda.git'
        local_path_prefix = '/tmp'
        local_path = os.path.join(local_path_prefix, 'phlambda')
        # 从bitbucket下载代码 存放在local_path下
        repo = GitRepository(local_path, git_url, branch='PBDP-1871-lambda-directory-code-build')

        # 打包上传代码
        zip_code(local_path)

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
    event = {'resource': '/integration', 'path': '/integration', 'httpMethod': 'POST', 'headers': {'X-Event-Key': ' repo:refs_changed', 'X-Request-Id': ' df1fd937-b664-4973-ba9b-33935a473c18', 'Content-Type': ' application/json; charset=utf-8'}, 'multiValueHeaders': {'X-Event-Key': [' repo:refs_changed'], 'X-Request-Id': [' df1fd937-b664-4973-ba9b-33935a473c18'], 'Content-Type': [' application/json; charset=utf-8']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'gqk3k1', 'resourcePath': '/integration', 'httpMethod': 'POST', 'extendedRequestId': 'FvvC8EbH5PgF2mQ=', 'requestTime': '16/Sep/2021:07:55:37 +0000', 'path': '/integration', 'accountId': '444603803904', 'protocol': 'HTTP/1.1', 'stage': 'test-invoke-stage', 'domainPrefix': 'testPrefix', 'requestTimeEpoch': 1631778937072, 'requestId': '963a3249-dbc0-479e-849b-2a556093388e', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'test-invoke-api-key', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': 'arn:aws-cn:sts::444603803904:assumed-role/Ph-Data-Resource-Admin/hbzhao', 'apiKeyId': 'test-invoke-api-key-id', 'userAgent': 'aws-internal/3 aws-sdk-java/1.12.59 Linux/5.4.134-73.228.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.302-b08 java/1.8.0_302 vendor/Oracle_Corporation cfg/retry-mode/standard', 'accountId': '444603803904', 'caller': 'AROAWPBDTVEAK3O5OG5QB:hbzhao', 'sourceIp': 'test-invoke-source-ip', 'accessKey': 'ASIAWPBDTVEAMR2G2J4L', 'cognitoAuthenticationProvider': None, 'user': 'AROAWPBDTVEAK3O5OG5QB:hbzhao'}, 'domainName': 'testPrefix.testDomainName', 'apiId': '2t69b7x032'}, 'body': '{"eventKey":"repo:refs_changed","date":"2021-09-16T15:49:11+0800","actor":{"name":"hbzhao","emailAddress":"hbzhao@data-pharbers.com","id":302,"displayName":"赵浩博","active":true,"slug":"hbzhao","type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/users/hbzhao"}]}},"repository":{"slug":"phlambda","id":13,"name":"phlambda","scmId":"git","state":"AVAILABLE","statusMessage":"Available","forkable":true,"project":{"key":"LGC","id":25,"name":"logic","description":"业务逻辑层","public":false,"type":"NORMAL","links":{"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC"}]}},"public":false,"links":{"clone":[{"href":"https://bitbucket.pharbers.com/scm/lgc/phlambda.git","name":"http"},{"href":"ssh://git@bitbucket.pharbers.com:7999/lgc/phlambda.git","name":"ssh"}],"self":[{"href":"https://bitbucket.pharbers.com/projects/LGC/repos/phlambda/browse"}]}},"changes":[{"ref":{"id":"refs/heads/PBDP-1871-lambda-directory-code-build","displayId":"PBDP-1871-lambda-directory-code-build","type":"BRANCH"},"refId":"refs/heads/PBDP-1871-lambda-directory-code-build","fromHash":"6e0736f64e7ab1e544d3a70c6a5c329f1a598006","toHash":"316d78803f680faf88da4a91764f03eb87a62fd6","type":"UPDATE"}]}\n', 'isBase64Encoded': False}

    lambda_handler(event=event, context=None)
