import json
import boto3
from boto3.dynamodb.conditions import Key


'''
删除创建的中间文件，文件都从 dynamodb 找，并按照规则拼出路径
args = {
    "traceId": "alfred-resource-creation-traceId",
    "projectId": "ggjpDje0HUC2JW",
    "projectName": "demo",
    "owner": "alfred",
    "showName": "alfred"
}
'''


def lambda_handler(event, context):
    return True

