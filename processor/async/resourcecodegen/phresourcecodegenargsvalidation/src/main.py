import json
import boto3
from boto3.dynamodb.conditions import Attr, Key

'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "flowVersion": "developer",
        "dagName": "demo",
        "owner": "hbzhao",
        "showName": "赵浩博"
    },
    "action": {
        "cat": "createDataset",
        "desc": "create intermediate dataset",
        "comments": "something need to say",
        "message": "something need to say",
        "required": true
    },
    "script": {
        "id": "",
        "jobName": "",
        "jobPath": "",
        "inputs": [],           // 现在没用，可能以后有用
        "outputs": []           // 现在没用，可能以后有用
    },
    "steps": [                  // 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
        {
            "stepId": "1",
            "ctype": "FillEmptyWithValue",
            "expressions": {
                "type":"FillEmptyWithValue",
                "code":"pyspark",
                "params":{
                    "columns":["订单内件数"],
                    "value":"4"
                }
            }
        },
        {
            "stepId": "2",
            "ctype": "FillEmptyWithValue",
            "expressions": {
                "type":"FillEmptyWithValue",
                "code":"pyspark",
                "params":{
                    "columns":["订单内件数"],
                    "value":"4"
                }
            }
        },
    ],
    "notification": {
        "required": true
    },
    "result": {
        "OldImage": [
            // 这个地方特别需要注意，保存steps修改前数据库的样子
        ]
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

        if not data.get("script"):
            raise Exception('script not exits')

        steps = data.get("steps", "")
        if not isinstance(steps, list):
            raise Exception('setps error')

        return True


def lambda_handler(event, context):
    return Check().check_parameter(event)
    # 1. common 必须存在
    # 2. action 必须存在
    # 3. notification 必须存在
    # 4. script 必须存在一个
    # 5. steps 必须存在，可以是空数组
