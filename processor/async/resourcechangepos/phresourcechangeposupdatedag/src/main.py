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
            "inputs": {
                    "old": [{
                        "name": "A",
                        "cat": "uploaded"
                    }],
                    "new": [{
                        "name": "B",
                        "cat": "uploaded"
                    }]
                }
            "output": {
                    "old": {
                        "name": "A_out",
                        "cat": "intermediate"
                    },
                    "new": {
                        "name": "B_out",
                        "cat": "intermediate"
                    }
                }
            
        }
        
        
    },
return:
    {
        "deleteItems":[
            {}
        ],
        "insertItems":[
            {}
        ]
    }
'''


def get_all_item_from_dag(projectId):
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        KeyConditionExpression=Key("projectId").eq(projectId)
    )
    return res.get("Items")


def lambda_handler(event, context):
    # 获取所有的project items
    all_dag_items = get_all_item_from_dag(event["projectId"])
    # 判断脚本输入dataset的inputs
    deleteItems = []
    insertItems = []
    # 处理旧的输入ds
    old_input_ds_name = list(old_ds["name"] for old_ds in event["datasets"]["inputs"]["old"])
    new_input_ds_name = list(new_ds["name"] for new_ds in event["datasets"]["inputs"]["new"])
    
    return 1
