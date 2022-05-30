import json
import boto3
from boto3.dynamodb.conditions import Key


'''
这个函数是对所有的reboot的数据参数的validate
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "tenantStop",
        "desc": "reboot project",
        "comments": "something need to say",
        "message": "something need to say",
        "required": true
    },
    "notification": {
        "required": true
    }
}
'''


def lambda_handler(event, context):
    return True

