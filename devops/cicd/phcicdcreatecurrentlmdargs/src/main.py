import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')
'''
将错误提取出来写入到notification中
args:
    event = {
        "lambda": [
            {   
                "action": "creation",
                "name": "functionName + codebuild"
                "functionPath": "",
                "cfn": "codebuildS3Path",
                "parameters": {
                    "functionName": "",
                    "branchName"："",
                    "repoName": "",
                    "alias": "",
                    "gitUrl": ""
                }
            }, {...}
        ],
        "sfn": {
            "stateMachineName": "",
            "submitOwner": "",
            "s3Bucket": "",
            "s3TemplateKey": ""
        }
    }
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


def lambda_handler(event, context):
    print(event)
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

    # 创建失败的 notification message
    message = {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": "{}",
            "error": json.dumps(event["errors"])
        }
    }
    return message
