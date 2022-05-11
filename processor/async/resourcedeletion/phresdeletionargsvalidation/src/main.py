import json
import boto3
from boto3.dynamodb.conditions import Attr

'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "common": {
            "traceId": "alfred-resource-creation-traceId",
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred"
        },
        "action": {
            "cat": "createDataset",
            "desc": "create intermediate dataset",
            "comments": "something need to say",
            "message": "something need to say",
            "required": true
        },
        "datasets": [
            {
                "name": "test_name"
            }
        ],
        "script": {
            "actionName": "compute_C2",
        },
        "notification": {
            "required": true
        }
    }
'''

def lambda_handler(event, context):
    print(event)
    # return Check().check_parameter(event)

    # 1. common 必须存在
    # 2. action 必须存在
    # 3. notification 必须存在
    # 4. datasets 和 scripts 必须存在一个
    #   4.1 如果dataset存在，name 都必须存在，并判断类型
    #   4.2 如果scripts存在，actionName 都必须存在，并判断类型
    # 5. 输入的datasets name 必须存在
    # 6. 输入的script 的 actionName 必须存在
    return True
