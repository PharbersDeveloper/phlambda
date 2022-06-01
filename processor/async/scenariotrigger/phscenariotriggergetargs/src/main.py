import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
从Scenario dynamodb中 获取detail
然后处理成executionV2 trigger的参数
{"type": "dataset", "recursive": false, "ignore-error": false, "name": "1235"}	
args:
    event = {
        "scenarioId.$": "$.scenario.scenarioId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "tenantId.$": "$.common.tenantId",
        
        "scenario.$": {
            "id": "scenario id",
            "active": true,
            "scenarioName": "scenario name",
            "deletion": false, --舍弃
            "index": "index"
        }
    }
'''


def lambda_handler(event, context):

    return 1


