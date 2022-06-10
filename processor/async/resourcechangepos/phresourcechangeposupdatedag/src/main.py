import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
'''
将错误提取出来写入到notification中
args:
    event = {
        "traceId": "traceId",
        "projectId": "projectId",
        "projectName": "projectName",
        "owner": "owner",
        "showName": "showName",
        "datasets": {
            "input": [
            {
                "old": {
                    "name": "A",
                    "cat": "uploaded"
                },
                "new": {
                    "name": "B",
                    "cat": "uploaded"
                }
            },
            {
                "old": {
                    "name": "A_out",
                    "cat": "intermediate"
                },
                "new": {
                    "name": "B_out",
                    "cat": "intermediate"
                }
            }
        ]
        }
        
        
    },
return:
    {
        "dagItems": [{
                "old": {},
                "new": {}
            },
            {
                "old": {},
                "new": {}
            }
        ]
    }
'''


def get_item_from_dag(name, projectId):
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        IndexName='dag-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").eq(name)
    )
    return res.get("Items")


def lambda_handler(event, context):
    # 根据参数找到item 修改item的 name runtime traceId
    for dataset in event["datasets"]:
    return 1
