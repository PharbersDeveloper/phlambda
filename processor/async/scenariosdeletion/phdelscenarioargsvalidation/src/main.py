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
            "cat": "createOrUpdateScenario",
            "desc": "create or update scenario",
            "comments": "something need to say",
            "message": "something need to say",
            "required": true
        },
        "notification": {
            "required": true      
        },
        "scenario": {
            "id": "scenario id",       
            "active": true,
            "scenarioName": "scenario name"
        },
        "triggers": [
            {
                "active": true,
                "detail": {
                    "timezone":"中国北京",
                    "start":"2022-04-26 16:10:14",
                    "period":"minute",
                    "value":1
                },
                "index": 0,
                "mode": "timer",
                "id": "trigger id",       # 如果有就是update，如果没有就是新建
            }
        ],
        "steps": [
            {
                "confData": {},
                "detail": {
                    "type":"dataset",
                    "recursive":false,
                    "ignore-error":false,
                    "name":"1235"
                },
                "index": 0,
                "mode": "dataset",,
                "name": "alfred"
                "id": "step id",       # 如果有就是update，如果没有就是新建
            }
        ]
    }
'''


def lambda_handler(event, context):
    # 1. common 必须存在
    # 2. action 必须存在
    # 3. notification 必须存在
    # 4. scenario triggers 和 steps 必须存在一个, 存在哪个就删除哪个
    return True