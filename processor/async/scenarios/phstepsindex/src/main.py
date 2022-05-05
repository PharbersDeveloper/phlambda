import json
import boto3
from boto3.dynamodb.conditions import Attr

'''
这个函数只做一件事情，将 scenario steps 的所有东西写到 scenario_step dynamodb中
args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": {
            "id": "scenario id",
            "active": true,
            "scenarioName": "scenario name",
            "deletion": false
        },
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
                "mode": "dataset",
                "name": "alfred",
                "id": "step id",
            }
        ]
    }
'''

def lambda_handler(event, context):
    return true
