import json
import math
import random
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
'''
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
            
        },
        script: {
            "old": {
                "name": compute_A,
                "id": "22jpN8YtMIhGTnW"
            },
            "new": {
                "name": "compute_B",
                "runtime": "python",
                "inputs": "[\"B\"]",
                "output": "compute_B"
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


def generate():
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
              "abcdefghijklmnopqrstuvwxyz" \
              "0123456789"
    charsetLength = len(charset)
    keyLength = 3 * 5
    array = []
    for i in range(keyLength):
        array.append(charset[math.floor(random.random() * charsetLength)])

    return "".join(array)


def create_link_item(projectId, sortVersion, cat, cmessage, ctype, flowVersion, level, name, position, prop, representId,
                 runtime, traceId):

    Item = {
        "projectId": projectId,
        "sortVersion": sortVersion,
        "cat": cat,
        "cmessage": cmessage,
        "ctype": ctype,
        "flowVersion": flowVersion,
        "level": level,
        "name": name,
        "position": position,
        "prop": prop,
        "representId": representId,
        "runtime": runtime,
        "traceId": traceId
    }

    return Item


def get_all_item_from_dag(projectId):
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        KeyConditionExpression=Key("projectId").eq(projectId)
    )
    return res.get("Items")


def lambda_handler(event, context):
    # 获取所有的project items
    all_dag_items = get_all_item_from_dag(event["projectId"])
    all_link_dag_items = list(item for item in all_dag_items if item["ctype"] == "link")
    # 判断脚本输入dataset的inputs
    deleteLinkItems = []
    insertLinkItems = []
    # 处理旧的输入ds
    old_input_ds_names = list(old_ds["name"] for old_ds in event["datasets"]["inputs"]["old"])
    # 处理新的输入ds
    new_input_ds_names = list(new_ds["name"] for new_ds in event["datasets"]["inputs"]["new"])
    # 处理旧的输出ds
    old_output_ds_name = event["datasets"]["output"]["old"]["name"]
    # 处理新的输出ds
    new_output_ds_name = event["datasets"]["output"]["new"]["name"]
    # 获取好name后处理link
    # 所有cmessage含有script id的需要删除
    job_id = event["script"]["old"]["id"]
    deleteLinkItems = list(item for item in all_link_dag_items if json.loads(item["cmessage"])["sourceId"] == job_id or json.loads(item["cmessage"])["targetId"] == job_id)
    # 然后重新创建link
    # 创建input到job link
    new_input_ds_msg = list({"name": item["name"], "representId": item["representId"]} for item in all_dag_items if item["name"] in new_input_ds_names)
    for input_ds_msg in new_input_ds_msg:
        input_link_represent_id = generate()
        cmessage = {
            "sourceId": input_ds_msg["representId"],
            "sourceName": input_ds_msg["name"],
            "targetId": job_id,
            "targetName": event["script"]["new"]["name"]
        }
        create_link_item(event["projectId"], "developer_" + input_link_represent_id, "")

    # 创建job到output link
    new_output_ds_msg = list({"name": item["name"], "representId": item["representId"]} for item in all_dag_items if item["name"] == new_output_ds_name)
    new_output_link_id = generate()
    cmessage = {
        "sourceId": job_id,
        "sourceName": event["script"]["new"]["name"],
        "targetId": new_output_ds_msg["representId"],
        "targetName": new_output_ds_msg["name"]
    }

    return 1
