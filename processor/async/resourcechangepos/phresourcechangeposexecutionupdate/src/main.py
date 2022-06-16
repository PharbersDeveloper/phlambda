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
                "script": {
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
                "jobName": delete_item["jobName"]
            }
        )

    for insert_item in scriptItems["insertItems"]:
        res = dagconf_table.put_item(
            Item=insert_item
        )


def create_script_file_args(event):

    code_gen_args = create_code_gen_args(event)
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
            "cat": "renameScript",
            "desc": "renameScript",
            "comments": "something need to say",
            "message": json.dumps("renameScript", ensure_ascii=False),
            "required": True
        },
        "script": {
            "name": event["script"]["new"]["name"],
            "flowVersion": "developer",
            "runtime": event["script"]["new"]["runtime"],
            "inputs": event["script"]["new"]["inputs"],
            "output": event["script"]["new"]["output"],
            "version": [],
            "id": event["script"]["old"]["id"],
            "isCreation": False
        },
        "codeGenArgs": code_gen_args,
        "notification": {
            "required": True
        },
        "result": {}
    }

    return args


def create_code_gen_args(event):
    message = {
        "optionName": "sync_edit",
        "cat": "intermediate",
        "runtime": event["script"]["new"]["runtime"],
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
            "cat": "changeResourcePosition",
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
            "runtime": event["script"]["new"]["runtime"]
        },
        "steps": [],
        "notification": {
            "required": True
        },
        "oldImage": []
    }

    return args


def create_copy_script_file_args(event):

    changeScriptMsg = event["script"]
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
            "cat": "renameScript",
            "desc": "renameScript",
            "comments": "something need to say",
            "message": json.dumps("renameScript", ensure_ascii=False),
            "required": True
        },
        "script": {
            "name": event["script"]["new"]["name"],
            "flowVersion": "developer",
            "runtime": event["script"]["new"]["runtime"],
            "inputs": event["script"]["new"]["inputs"],
            "output": event["script"]["new"]["output"],
            "version": [],
            "id": event["script"]["old"]["id"],
            "isCreation": False
        },
        "changeScriptMsg": changeScriptMsg,
        "notification": {
            "required": True
        },
        "result": {}
    }

    return args


def lambda_handler(event, context):
    print(event)
    # 获取需要更新的dag Items
    update_dag_item(event["dagItems"])
    # 获取需要更新的dag conf Items
    update_dagconf_item(event["scriptItems"])
    if event["script"]["new"]["runtime"] == "prepare":
        # 创建触发code gen参数
        args = create_script_file_args(event)
    else:
        # 创建触发copy script file 参数
        args = create_copy_script_file_args(event)

    return args
