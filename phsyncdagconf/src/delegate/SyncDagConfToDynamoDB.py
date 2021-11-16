import os
import json
from util.AWS.DynamoDB import DynamoDB


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
                print(item)
                self.dynamodb.putData({
                    "table_name": "project_files",
                    "item": item
                })

        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
                },
                "body": json.dumps({
                    "message": "server error;" + e
                })
            }

        # return {
        #     "statusCode": 200,
        #     "headers": {
        #         "Access-Control-Allow-Headers": "Content-Type",
        #         "Access-Control-Allow-Origin": "*",
        #         "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        #     },
        #     "body": json.dumps(json_api_data)
        # }
