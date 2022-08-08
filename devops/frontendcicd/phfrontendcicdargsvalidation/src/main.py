import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "common": {
            "version": "0-0-1",
            "publisher": "赵浩博",
            "runtime": "prod"
        },
        "frontend": {
            "branch": "PBDP-3235-cicd",
            "commit": "184d0599303ccaa537417610c0dd6b929fe3a8a5",
            "repo": "micro-frontend",
            "components": [
                {
                "prefix": "client-helper/offweb-model-helper"
                }
            ],
            "required": true
        }
    }
'''


def check_parameter(event):
    # 1. common 必须存在
    if not event.get("common"):
        raise Exception('common must exist')
    # 2. frontend 必须存在
    if not event.get("common"):
        raise Exception('common must exist')
    return True


def lambda_handler(event, context):
    print(event)
    return check_parameter(event)

