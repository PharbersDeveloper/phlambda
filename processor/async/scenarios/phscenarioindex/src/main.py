import json
import boto3
from boto3.dynamodb.conditions import Attr

'''
这个函数只做一件事情，将scenario的所有东西写到Scenario dynamodb中
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
        }
    }
'''

def lambda_handler(event, context):
    return true
