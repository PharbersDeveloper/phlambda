import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
from pherrorlayer import *


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
                "errors": {
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
    for delete_item in dagItems["insertItems"]:
        dag_table.delete_item(
            Key={
                "projectId": delete_item["projectId"],
                "sortVersion": delete_item["sortVersion"]
            }
        )

    for insert_item in dagItems["deleteItems"]:
        res = dag_table.put_item(
            Item=insert_item
        )


def update_dagconf_item(scriptItems):

    dagconf_table = dynamodb.Table('dagconf')
    for delete_item in scriptItems["insertItems"]:
        dagconf_table.delete_item(
            Key={
                "projectId": delete_item["projectId"],
                "jobName": delete_item["jobName"]
            }
        )

    for insert_item in scriptItems["deleteItems"]:
        res = dagconf_table.put_item(
            Item=insert_item
        )


def update_step_item(stepItem):

    step_table = dynamodb.Table('step')
    delete_item = stepItem["insertItems"]
    step_table.delete_item(
        Key={
            "projectId": delete_item["projectId"],
            "jobName": delete_item["jobName"]
        }
    )

    res = step_table.put_item(
        Item=stepItem["deleteItems"]
    )


def errors_adapter(error):
    error = json.loads(error)
    Command = {
        "common_must_exist": ParameterError,
        "action_must_exist": ParameterError,
        "action.cat_must_be_changeResourcePosition": ParameterError,
        "script_item_must_exist": ParameterError,
        "item_must_exist": ParameterError,
        "errors": Errors
    }
    errorMessage = error.get("errorMessage").replace(" ", "_")
    errorMessage = "item_must_exist" if "item must exist" in errorMessage else errorMessage

    if errorMessage in Command.keys():
      return serialization(Command[errorMessage])
    else:
      return serialization(Command["errors"])



def lambda_handler(event, context):
    print(event)
    errors = event.get("errors")
    # item处理
    # 恢复dag表中已经删除的item
    # 删除dag表中已经创建的item
    if event.get("dagItems"):
        update_dag_item(event["dagItems"])
    # 恢复dagconf表中已经删除的item
    # 删除dagconf表中已经删除的item
    if event.get("scriptItems"):
        update_dagconf_item(event["scriptItems"])
    # 删除s3上脚本路径上的文件
    if event.get("stepItems"):
        update_dagconf_item(event["stepItems"])
    # 创建失败的 notification message
    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": "{}",
            "error": errors_adapter(errors.get("Cause"))
        }
    }
