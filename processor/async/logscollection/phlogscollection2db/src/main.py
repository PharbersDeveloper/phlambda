import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

'''
这个函数是对所有的写入log path
args = {
    "traceId": "alfred-resource-creation-traceId",
    "projectId": "ggjpDje0HUC2JW",
    "projectName": "demo",
    "owner": "alfred",
    "showName": "alfred",
    "jobName": "",
    "clusterId": "",
    "stepId": "",
    "result.$": "$.result"
}

return:
    result = {
        "logIsReady": false,
        "stepLogPath": "",
        "YarLogPath": "",
        "LambdaLogPath": ""
    }
'''


# 1. stackName 存在就删除
def lambda_handler(event, context):
    dt = datetime.now()
    ts = datetime.timestamp(dt) * 1000

    pn = event['projectName']
    jobShowName = event["jobName"]

    flowVersion = 'developer'
    tmpJobName = '_'.join([pn, pn, flowVersion, event['jobName']])

    execution_table = dynamodb.Table('execution')

    res = execution_table.query(
        IndexName='runnerId-jobName-index',
        KeyConditionExpression=Key("runnerId").eq(event["runnerId"])
                               & Key("jobName").begins_with(tmpJobName)
    )
    item = res["Items"][0]

    logs = []
    for iter in event["result"].keys():
        if iter == "logIsReady":
            continue

        logs.append({
            "type": iter,
            "uri": event["result"][iter]
        })

    # 更改status和endAt
    item.update({"endAt": str(int(ts))})
    item.update({"status": "success"})
    item.update({"logs": json.dumps(logs)})

    response = execution_table.put_item(
        Item=item
    )
    return response
