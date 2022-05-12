import json
import boto3

'''
这个函数只做一件事情，在现有pyspark的脚本上重新创建。记住每次都是重新创建，基于steps的全image
********** 是镜像流程，不是插入删除流程 *********
Join 流程
args:
    event = { 
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "flowVersion": "developer",
        "dagName": "demo",
        "owner": "hbzhao",
        "showName": "赵浩博",
        "script": {
            "id": "",
            "jobName": "",
            "jobPath": "",
            "inputs": [],           // 现在没用，可能以后有用
            "outputs": [],          // 现在没用，可能以后有用
            "runtime": "prepare"
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
        ]
    }
'''

def lambda_handler(event, context):
    return true
