import json
import boto3

'''
logs collection 的参数 validation
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "clusterId": "String",
    "stepId": "String",
    "jobName": "",
    "date": "Integer"   // in seconds
}
'''


def lambda_handler(event, context):
    # 1. clusterId 必须存在
    # 2. stepId 必须存在
    # 3. jobName 必须存在
    # 4. date 必须存在，并且时间在当前时间之后
    return True
