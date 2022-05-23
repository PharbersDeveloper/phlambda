import json
import boto3

'''
理论上只有超时才会走到这里
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "clusterId": "",
    "stepId": ""
}
'''


# 1. stackName 存在就删除
def lambda_handler(event, context):
    return True
