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

class Check:
    def check_parameter(self, data):

        # 1. common 必须存在
        if not data.get("common"):
            raise Exception('common not exits')

        # 2. action 必须存在
        if not data.get("action"):
            raise Exception('action not exits')

        # 3. notification 必须存在
        if not data.get("notification"):
            raise Exception('notificaiton not exits')

        return True


def lambda_handler(event, context):
    return Check().check_parameter(event)

