import json
import boto3
from boto3.dynamodb.conditions import Attr

'''
这个函数只做一件事情，从输入参数中，按照产品逻辑的到需要删除的脚本与links
核心从dynamodb 的dag表中得到需要删除的关联信息
并将结果详细信息返回，给后面的lambda使用

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "datasets.$": "$.datasets",
        "script.$": "$.script"
    }

return:
    {
        "result": {
            "datasets": {
                "id": "",
                ....
            },
            "stript": {
                "id": "",
                ....
            },
            "links": {
                "id": "",
                ....
            }
        }
    }
'''

def lambda_handler(event, context):
    return {
        "datasets": {
            "id": "",
        },
        "stript": {
            "id": "",
        },
        "links": {
            "id": "",
        }
    }
