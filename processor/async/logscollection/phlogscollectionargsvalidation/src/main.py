import json
import time

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


def check_parameter(data, **kwargs):
    # 1. clusterId 必须存在
    if not data.get("clusterId"):
        raise Exception('clusterId not exits')

    # 2. stepId 必须存在
    if not data.get("stepId"):
        raise Exception('stepId not exits')

    # 3. jobName 必须存在
    if not data.get("jobName"):
        raise Exception('jobName not exits')

    # 4. date 必须存在，并且时间在当前时间之后
    datetime = data.get("date")
    if not datetime or int(datetime) > int(time.time()):
        raise Exception('datatime not exits or not True')

    return True


def lambda_handler(event, context):
    return check_parameter(event)
    # 1. clusterId 必须存在
    # 2. stepId 必须存在
    # 3. jobName 必须存在
    # 4. date 必须存在，并且时间在当前时间之后
