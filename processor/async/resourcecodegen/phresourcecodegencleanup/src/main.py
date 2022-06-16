import json
import boto3

'''
这个函数只做一件事情，恢复steps oldimage
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
        ],
        "error": {
            "Error": "",
            "Cause": ""
        }
    }
'''


class CleanUp:
    dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1")
    table = dynamodb.Table("step")

    def put_item(self, item):
        response = self.table.put_item(
            Item=item
        )

    def del_item(self, pjName, stepId):
        self.table.delete_item(
            Key={
                "pjName": pjName,
                "stepId": stepId
            }
        )

    def run(self, steps, oldImage, ifsteps, **kwargs):
        for step in steps:
            pjName = step.get("pjName")
            stepId = step.get("stepId")
            self.del_item(pjName, stepId)
        if ifsteps:
            for step in oldImage:
                self.put_item(step)


def lambda_handler(event, context):
    errors = event.get("errors")
    print(event)
    CleanUp().run(**event)
    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
        }
    }
