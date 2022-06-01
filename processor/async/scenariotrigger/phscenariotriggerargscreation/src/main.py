import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
通过
args:
    event = {
            "projectId": "ggjpDje0HUC2JW",
            "tenantId": "zudIcG_17yj8CEUoCTHg",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred",
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

return:
        {
            "Iterator": "",
            "currentScenarioStep": "",
            "scenarioSteps": ""
        }
'''


def lambda_handler(event, context):

    return 1
