import json
import boto3
from boto3.dynamodb.conditions import Attr

'''
删除ds相关的数据信息
1. 一定是 先删除 clickhouse 中的 sample
2. 再删除 S3 中的数据

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "resources": {
    
        },
        "datasets.$": [{
            "id": "",
                ....
        }]
    }
'''

def lambda_handler(event, context):
    return true
