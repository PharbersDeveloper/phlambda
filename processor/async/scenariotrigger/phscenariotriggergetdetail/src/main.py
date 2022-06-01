import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
需要通过scenarioId从dynamodb表scenario_step获取
当前scenarioId下的所有item并根据index排序返回details
args:
    event = {
            "scenarioId": "ggjpDje0HUC2JW_f06f093f8f684289b949335e5e48edcd",
            "projectId": "ggjpDje0HUC2JW"
    }

return:
    {
        "scenarioSteps": [
            {
                "detail": {
                    "type": "dataset",
                    "recursive": false, 
                    "ignore-error": false, 
                    "name": "1235"
                }
            }，
            {
                ...
            }
        ]
    }
'''


def lambda_handler(event, context):

    return 1
