import json
import random
import math
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


def put_dataset_item(id, projectId, name, label, schema, path, format, cat, prop, sample="F_1", dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('notification')

    res = table.query(
        KeyConditionExpression=Key("id").eq(projectId)
                               & Key("projectId").begins_with(name)
    )

    response = {}
    if len(res["Items"]) == 0:
        response = table.put_item(
            Item={
                "id": id,
                "projectId": projectId,
                "name": name,
                "label": label,
                "schema": schema,
                "path": path,
                "format": format,
                "cat": cat,
                "prop": prop,
                "sample": sample,
            }
        )

    return response


def lambda_handler(event, context):
    print("输入event")
    print(event)
    print("================>>>>>>>>>>>>>")
    
    # 1. 只做一件事情，写dataset dynamodb，id在这里创建

    result = []
    for dataset in event["datasets"]:
        id = generate()
        dataset.update({"id": id})
        result.append(dataset)
        put_dataset_item(id, event["projectId"], event["datasets"]["name"], label="[]", schema="[]", path="",
                         format=event["datasets"]["format"], cat=event["datasets"]["cat"], prop="")

    return {
        result
    }
