import json
import math
import random
import boto3

'''
这个函数做一件事情，写dagconf dynamodb
args = {
    "traceId": "String",
    "projectId": "String",
    "projectName": "String",
    "owner": "String",
    "showName": "String",
    "script": {
        "runtime": "pyspark"
        "actionName": "compute_C2",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
    }
}

return =  
    {
        "id": "String",                 # 生成的ID
        "jobName": "String",
        "actionName": "String",
        "flowVersion": "developer",
        "inputs": "[]",
        "output": "{}"
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


def put_dagconf_item(id, projectId, actionName, projectName, flowVersion, inputs, outputs, labels, owner,
                     operatorParameters, runtime, prop, showName, timeout, dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dagconf')

    jobDisplayName = "_".join(projectName, projectName, flowVersion, actionName)
    jobName = "_".join(flowVersion, id, jobDisplayName)
    response = table.put_item(
        Item={
            "id": id,
            "projectId": projectId,
            "jobName": jobName,
            "actionName": actionName,
            "dagName": projectName,
            "flowVersion": flowVersion,
            "inputs": inputs,
            "jobDisplayName": jobDisplayName,
            "jobId": id,
            "jobShowName": actionName,
            "jobVersion": flowVersion,
            "labels": labels,
            "operatorParameters": operatorParameters,
            "outputs": outputs,
            "owner": owner,
            "projectName": projectName,
            "runtime": runtime,
            "prop": prop,
            "showName": showName,
            "timeout": timeout,
        }
    )

    return response


def lambda_handler(event, context):
    print("输入event")
    print(event)
    print("================>>>>>>>>>>>>>")
    # 1. 只做一件事情，写dagconf dynamodb，id在这里创建
    id = generate()
    put_dagconf_item(id, event["projectId"], event["script"]["actionName"], event["projectName"], event["script"]["flowVersion"], event["inputs"], event["outputs"], "", event["owner"],
                     "", event["script"]["runtime"], "", event["showName"], 1000)

    result = event["script"].update({"id": id})

    return result
