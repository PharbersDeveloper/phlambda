import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')
'''
处理lmd和sfn的相关信息
args:
    event = {
        "common": {
            "version": "version",
            "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
            "publisher": "赵浩博",
            "alias": "hbzhao-resource-change-position-owner",
            "runtime": "dev/v2/prod"
        },
        "processor": {
            "repo": "phlambda",
            "branch": "",
            "prefix": "processor/async/createscriptrefile",
            "stateMachineName": "createscriptrefile",
            "sm": "processor/async/createscriptrefile/sm.json",
            "functions": [
                {   
                    "name": "phresourcepycodegen"
                },
                {
                    "name": "phresourcercodegen"
                }
            ]
            "required": true
        }
return:
    {
        "lambda": [
            {
                "functionPath": "",
                "functionName": "",
                "branchName"："",
                "repoName": "",
                "alias": ""
            }, {...}
        ],
        "sfn": {
            "stateMachineName": "",
            "submitOwner": "",
            "s3Bucket": "",
            "s3TemplateKey": ""
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
