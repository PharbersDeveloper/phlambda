import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "common": {
            "traceId": "alfred-resource-creation-traceId",
            "projectId": "ggjpDje0HUC2JW",
            "tenantId": "zudIcG_17yj8CEUoCTHg",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred"
        },
        "action": {
            "cat": "scenarioTrigger",
            "desc": "scenario trigger",
            "comments": "something need to say",
            "message": "something need to say",
            "required": true
        },
        "notification": {
            "required": true      
        },
        "scenario": {
            "scenarioId": "scenario id",       
        }
    }
'''


def lambda_handler(event, context):
    # 1. common 必须存在
    # 2. action 必须存在
    # 3. scenarioId 在 ScenarioStep 表中必须存在
    # 4. scenarioStep中 detail里的 name 必须在dag表中存在
    # 5. ssm 中必须存在 key 为 tenantId的项
    return True
