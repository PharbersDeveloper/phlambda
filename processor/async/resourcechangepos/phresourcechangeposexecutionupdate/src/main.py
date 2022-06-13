import json

import boto3
dynamodb = boto3.resource('dynamodb')

'''
将错误提取出来写入到notification中
args:
    event = {
                "projectId": "ggjpDje0HUC2JW",
                "traceId": "",
                "projectName": "demo",
                "owner": "alfred",
                "showName": "alfred",
                "dagItems":{
                    "deleteItems": deleteItems,
                    "insertItems": insertItems
                },
                "scriptItems":{
                    "deleteItems": deleteItems,
                    "insertItems": insertItems
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
                        "output": "B_out"
                    }
                }
            },
return:
    {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
    }
}
'''


def update_dag_item(dagItems):

    dag_table = dynamodb.Table('dag')
    for delete_item in dagItems["deleteItems"]:
        dag_table.delete_item(
            Key={
                "projectId": delete_item["projectId"],
                "sortVersion": delete_item["sortVersion"]
            }
        )

    for insert_item in dagItems["insertItems"]:
        res = dag_table.put_item(
            Item=insert_item
        )


def update_dagconf_item(scriptItems):

    dagconf_table = dynamodb.Table('dagconf')
    for delete_item in scriptItems["deleteItems"]:
        dagconf_table.delete_item(
            Key={
                "projectId": delete_item["projectId"],
                "sortVersion": delete_item["jobName"]
            }
        )

    for insert_item in scriptItems["insertItems"]:
        res = dagconf_table.put_item(
            Item=insert_item
        )


def create_code_gen_args(event):
    message = {
        "optionName": "sync_edit",
        "cat": "intermediate",
        "runtime": "sync",
        "actionName": event["script"]["new"]["name"]
    }
    args = {
        "common": {
            "traceId": event["traceId"],
            "projectId": event["projectId"],
            "projectName": event["projectName"],
            "flowVersion": "developer",
            "dagName": event["projectName"],
            "owner": event["owner"],
            "showName": event["showName"]
        },
        "action": {
            "cat": "editSync",
            "desc": "edit sync steps",
            "comments": "something need to say",
            "message": json.dumps(message, ensure_ascii=False),
            "required": True
        },
        "script": {
            "id": "",
            "jobName": event["script"]["new"]["name"],
            "jobPath": "",
            "inputs": json.loads(event["script"]["new"]["inputs"]),
            "outputs": [
                event["script"]["new"]["output"]
            ],
            "runtime": "sync"
        },
        "steps": [],
        "notification": {
            "required": True
        },
        "oldImage": []
    }

    return args


def lambda_handler(event, context):
    print(event)
    # 获取需要更新的dag Items
    update_dag_item(event["dagItems"])
    # 获取需要更新的dag conf Items
    update_dagconf_item(event["scriptItems"])
    # 创建触发code gen参数
    code_gen_args = create_code_gen_args(event)

    return code_gen_args
