import json
import boto3
from boto3.dynamodb.conditions import Attr

'''
删除 script 相关的数据信息
1. 一定是 先删除 clickhouse 中的 sample ******* Script 也是有sample的 ********
2. 再删除 创建 脚本 以后会有git流程，现在直接操作s3（相当长的一段时间都会直接操作s3）

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "resources": {
    
        },
        "script": {
            "id": "",
                ....
        }
    }
'''

def lambda_handler(event, context):
    return true
