import json
import random
import math
import time
import boto3
from boto3.dynamodb.conditions import Key

'''
这个函数做一件事情写入dataset dynamodb
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "datasets": [
        {
            "name": "String",
            "cat": "intermediate",
            "format": "parquet"
        }
    ]
}

return = {
    [
        {
            "id": "String"         # 生成的Id
            "name": "String",
            "cat": "intermediate",
            "format": "parquet"
        }
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


def put_dataset_item(id, projectId, name, label, schema, path, format, cat, prop, traceId, sample="F_1",  dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table('dataset')

    res = ds_table.query(
        IndexName='dataset-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").eq(name)
    )

    response = {}
    print("dsName")
    print(name)
    if len(res["Items"]) == 0:
        print("putItem")
        response = ds_table.put_item(
            Item={
                "id": id,
                "date": str(int(round(time.time() * 1000))),
                "projectId": projectId,
                "name": name,
                "label": label,
                "schema": schema,
                "path": path,
                "format": format,
                "cat": cat,
                "prop": prop,
                "sample": sample,
                "traceId": traceId
            }
        )

    return response


def get_ds_representId(dsName, projectId):

    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        IndexName='dag-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").eq(dsName)
    )
    representId = ""
    if len(res["Items"]):
        representId = res["Items"][0].get("representId")

    return representId


def lambda_handler(event, context):
    print("输入event")
    print(event)
    print("================>>>>>>>>>>>>>")
    
    # 1. 只做一件事情，写dataset dynamodb，id在这里创建

    result = []
    if event["datasets"]:
        for dataset in event["datasets"]:
            # representId 需要从dag表先进行查询 如果有的则使用
            id = get_ds_representId(dataset["name"], event["projectId"])
            if not id:
                id = generate()
            dataset.update({"id": id})
            result.append(dataset)
            dataset_cat = dataset["cat"].lower()
            if dataset_cat == "shared" or dataset_cat == "export":
                put_dataset_item(id, event["projectId"], dataset["name"], label="[]", schema=dataset["schema"], path="",
                             format=dataset["format"], cat=dataset["cat"], prop="", traceId=event["traceId"])
            else:
                put_dataset_item(id, event["projectId"], dataset["name"], label="[]", schema=json.dumps(dataset["schema"], ensure_ascii=False), path="",
                             format=dataset["format"], cat=dataset["cat"], prop="", traceId=event["traceId"])
    print(result)
    return result

