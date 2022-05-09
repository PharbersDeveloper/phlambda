import json
import boto3
from boto3.dynamodb.conditions import Attr

'''
删除所有的dynamodb中的dataset表的索引记录
其中 links 是上一个lambda便利出来的详细的需要删除的 dag 表中的记录，包括node 和 link
resources 为从ssm中读取的数据

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "resources": {
    
        },
        "links.$": [{
            "id": "",
                ....
        }]
    }
'''

def lambda_handler(event, context):
    return true
