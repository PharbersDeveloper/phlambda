import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
在executionV2执行结束后获取执行的状态 
执行的状态通过runnerId 和 jobFullName从dynamodb获取
成功index+1
    如果index+1 == count scenario结束 status==succeed
    如果index+1 != count scenario继续 status==running
失败查看ignore-error参数
    如果为false scenario 结束 status == failed
    如果为true scenario继续 index+1 
        如果 index+1 == count scenario结束 status==succeed
        如果index+1 != count scenario继续 status==running
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
            "deletion": false, --舍弃
            "index": "index"
        }
    }
'''


def lambda_handler(event, context):

    return 1


