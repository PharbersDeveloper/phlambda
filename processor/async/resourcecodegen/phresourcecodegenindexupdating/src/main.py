import json
import boto3

'''
这个函数只做一件事情，将step写入数据库，然后将原有的数据写入oldimage
args:
    event = { 
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "flowVersion": "developer",
        "dagName": "demo",
        "owner": "hbzhao",
        "showName": "赵浩博",
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
        "OldImage": [
            // 这个地方特别需要注意，保存steps修改前数据库的样子
        ]
    }

return = [
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
'''

def lambda_handler(event, context):
    return true
