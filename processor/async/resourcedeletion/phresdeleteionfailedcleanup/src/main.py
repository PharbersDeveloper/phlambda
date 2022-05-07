import json
import boto3
from boto3.dynamodb.conditions import Attr

'''
这个函数实现两件事情：
1. 将错误的信息写入 notification 中
2. 将错误的被删除的 index 重新写回 dynamodb 中
    所有的信息都在 result 中存放

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "projectName.$": "$.common.projectName",
        "resources": {
    
        },
        "result": {
            "datasets": [{
                "id": "",
                ...
            }],
            "script": {
                "id": "",
                ...
            },
            "links": [{
                "id": "",
                ...
            }]
        }
    }
'''

def lambda_handler(event, context):
    return true
