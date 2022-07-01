import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "common": {
            "version": "version",
            "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
            "publisher": "赵浩博",
            "alias": "hbzhao-resource-change-position-owner",
            "runtime": "dev/v2/prod"
        },
        "processor": {
            "repo": "phlambda",
            "branch": "",
            "prefix": "processor/async/createscriptrefile",
            "stateMachineName": "createscriptrefile",
            "sm": "processor/async/createscriptrefile/sm.json",
            "functions": [
                {   
                    "name": "phresourcepycodegen"
                },
                {
                    "name": "phresourcercodegen"
                }
            ]
            "required": true
        },
        "trigger": {
            "repo": "phlambda",
            "branch": "",
            "prefix": "processor/sync/utils/phemail",
            "stateMachineName": "createscriptrefile",
            "name": "phemail"
            "entry": {
                "type": "ApiGateway",
                "resource": "",
                "method": ""
            }
            "required": true      
        }
    }
'''


def check_parameter(event):
    print(1)
    return True


def lambda_handler(event, context):
    print(event)
    return check_parameter(event)
    # 1. common 必须存在
    # 2. action 必须存在 cat 必须是 changeResourcePosition
    # 3. datasets 中的 old["name"] 必须在dag中查询到
    # 4. script中的 old id必须在dagconf表查询到
