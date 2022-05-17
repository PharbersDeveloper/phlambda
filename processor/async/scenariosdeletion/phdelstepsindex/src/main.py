import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from datetime import datetime

'''
删除steps里面的东西

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": "$.scenario",
        "steps.$": "$.steps"
    }
'''


def lambda_handler(event, context):
    return True
