import json
import boto3
import math
import random
from boto3.dynamodb.conditions import Key

'''
创建link
args = {
    "traceId": "String",
    "projectId": "String",
    "projectName": "String",
    "owner": "String",
    "showName": "String",
    "flowVersion": "developer",
    "datasets": [
        {
            "id": "String",
            "name": "String",
            "cat": "intermediate",
            "format": "parquet"
        }
    ]
    "script": {
        "id": "String",
        "jobName": "String",
        "runtime": "String",
        "name": "String",
        "flowVersion": "developer",
        "inputs": "["dsName"]",
        "output": "dsName"
    }
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


def get_ds_id(dsName, projectId):

    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table('dataset')
    res = ds_table.query(
        IndexName='dataset-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").begins_with(dsName)
    )
    dsId = ""
    if len(res["Items"]):
        dsId = res["Items"][0].get("id")
    else:
        raise Exception("dataset not found error")

    return dsId


def put_dag_item(projectId, sortVersion, cat, cmessage, ctype, flowVersion, level, name, position, prop, representId, runtime, dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dag')

    response = table.put_item(
        Item={
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
            "runtime": runtime
        }
    )

    return response


def lambda_handler(event, context):
    print("输入event")
    print(event)
    print("================>>>>>>>>>>>>>")

    # 创建dag 表的流程
    # 1 创建 dataset item
    for dataset in event["datasets"]:
        dsId = get_ds_id(dataset["name"], event["projectId"])
        sortVersion = event["flowVersion"] + "_" + dsId
        if dataset["cat"] == "catalog":
            prop = {"path": "", "partitions": 1, "format": "", "tableName": dataset["name"], "databaseName": "zudIcG_17yj8CEUoCTHg"}
            put_dag_item(event["projectId"], sortVersion, "dataset", "", "node", event["flowVersion"], "", dataset["name"],
                         "", json.dumps(prop, ensure_ascii=False), dataset["id"], dataset["cat"])
        else:
            prop = {"path": "", "partitions": 1}
            put_dag_item(event["projectId"], sortVersion, "dataset", "", "node", event["flowVersion"], "", dataset["name"],
                         "", json.dumps(prop, ensure_ascii=False), dataset["id"], dataset["cat"])

    # 2 创建 job item
    jobSortVersion = event["flowVersion"] + "_" + event["script"]["id"]
    put_dag_item(event["projectId"], jobSortVersion, "job", event["script"]["name"], "node", event["flowVersion"],
                 "", event["script"]["name"], "", "", event["script"]["id"], event["script"]["runtime"])

    # 3 创建 link item
    # 创建ds node 到 job node的 link
    for dataset in event["datasets"]:

        linkId = generate()
        linkSortVersion = event["flowVersion"] + "_" + linkId
        if dataset["name"] == event["script"]["output"]:
            # job -> output dataset
            cmessage = {
                "sourceId": event["script"]["id"],
                "sourceName": event["script"]["name"],
                "targetId": dataset["id"],
                "targetName": dataset["name"],
            }
        else:
            cmessage = {
                "sourceId": dataset["id"],
                "sourceName": dataset["name"],
                "targetId": event["script"]["id"],
                "targetName": event["script"]["name"],
            }
        put_dag_item(event["projectId"], linkSortVersion, "", json.dumps(cmessage), "link", event["flowVersion"],
                     "", "empty", "", "", linkId, "")


    return True
