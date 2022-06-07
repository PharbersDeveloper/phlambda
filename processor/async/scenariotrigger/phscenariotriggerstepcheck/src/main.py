import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
'''
在pharbers-trigger执行结束后获取执行的状态 
执行的状态通过runnerId 和 jobFullName从dynamodb获取
成功index+1
    如果index+1 == count -1 scenario结束 iterator.currentStatus==succeed
    如果index+1 != count -1 scenario继续 iterator.currentStatus==running
失败查看ignore-error参数
    如果为false scenario 结束 status == failed
    如果为true scenario继续 index+1 
        如果 index+1 == count -1 scenario结束 status==succeed
        如果index+1 != count -1 scenario继续 status==running
args:
    event = {
        "count": 2
        "runnerId": "demo_demo_developer_2022-06-06T07:01:02+00:00",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "c89b8123-a120-498f-963c-5be102ee9082",
        "showName": "赵浩博",
        "iterator": {
            "index": 0,
            "currentStatus": "running"
        },
        "scenarioStep": {
            "detail": {
                "type": "dataset",
                "recursive": false, 
                "ignore-error": false, 
                "name": "1235"
            },
            'confData': {}
        }

return:
    {
        "Iterator": {
            "index": ""
            "currentStatus": "running"
        }
    }
'''


def get_execution_status_from_execution(runnerId):
    execution_table = dynamodb.Table('execution')
    res = execution_table.query(
        IndexName='runnerId-jobName-index',
        KeyConditionExpression=Key("runnerId").eq(runnerId)
    )

    return res["Items"][0]["status"]


def execution_succeed(iterator, count):
    index = iterator["index"] + 1
    currentStatus = "succeed" if index == count else "running"

    iterator.update({"index": index})
    iterator.update({"currentStatus": currentStatus})

    return iterator


def execution_failed(iterator, count, ignoreError):
    # 失败查看ignore-error参数
    # 如果为false scenario 结束 status == failed
    # 如果为true scenario继续 index+1
    #   如果 index+1 == count -1 scenario结束 status==succeed
    #   如果index+1 != count -1 scenario继续 status==running
    if ignoreError:
        index = iterator["index"] + 1
        currentStatus = "succeed" if index == count else "running"
        iterator.update({"index": index})
        iterator.update({"currentStatus": currentStatus})
    else:
        iterator.update({"currentStatus": "failed"})

    return iterator


def lambda_handler(event, context):
    print(event)
    count = event["count"]
    ignoreError = event["scenarioStep"]["detail"]["ignore-error"]
    # 根据runnerId 获取执行状态
    execution_status = get_execution_status_from_execution(event["runnerId"])

    # 如果成功 index + 1
    if execution_status == "success":
        iterator = execution_succeed(event["iterator"], count)
    elif execution_status == "failed":
        iterator = execution_failed(event["iterator"], count, ignoreError)

    return iterator


