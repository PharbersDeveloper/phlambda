import os
import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
import time

class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()
        # import base64
        # from util.AWS.STS import STS
        # from constants.Common import Common
        # sts = STS().assume_role(
        #     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
        #     "Ph-Back-RW"
        # )
        # self.dynamodb = DynamoDB(sts=sts)

    def size_format(self, size):
        return '%.0f' % round(float(size/1024))

    def exec(self):
        event = self.event
        records = event["Records"]
        path = os.getenv("UPLOAD_PATH")
        try:
            data = []
            for record in records:
                print('EventID: ' + record['eventID'])
                print('EventName: ' + record['eventName'])
                if record["eventName"].lower() == "insert":
                    new_image = record["dynamodb"]["NewImage"]
                    item = {}
                    for field in list(new_image.keys()):
                        value = new_image[field]
                        v_k = list(value.keys())[0]
                        item[field] = value[v_k]
                    data.append(item)

            for item in data:
                id = item["id"]
                size = self.size_format(os.path.getsize(path + id))
                item["size"] = size
                item["status"] = "upload_succeed"
                print("Alex ====> \n")
                propertys = json.loads(item["property"])

                self.dynamodb.putData({
                    "table_name": "project_files",
                    "item": item
                })
                # TODO： 硬code + 无防御，有机会重构
                self.dynamodb.putData({
                    "table_name": "action",
                    "item": {
                        "id": GenerateID.generate(),
                        "projectId": propertys["projectId"],
                        "code": 0,
                        "comments": "",
                        "date": int(round(time.time() * 1000)),
                        "jobCat": "notification",
                        "jobDesc": "success",
                        "message": json.dumps({
                            "type": "notification",
                            "opname": propertys["opname"],
                            "opgroup": propertys["opgroup"],
                            "cnotification": {
                                "status": "upload_succeed",
                                "file": id
                            }
                        }),
                        "owner": propertys["opname"],
                        "showName": propertys["showName"]
                    }
                })

        except Exception as e:
            print(e)
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "server error;" + e
                })
            }
