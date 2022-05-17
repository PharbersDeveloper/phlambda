import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from datetime import datetime

'''
删除cloudformation 里面的东西 rule

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": "$.scenario",
        "triggers.$": "$.triggers"
    }
'''


def lambda_handler(event, context):
    return True
