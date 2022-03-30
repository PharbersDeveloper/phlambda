
import json
import time
import base64
from util.AWS.STS import STS
from constants.Common import Common
from util.AWS.DynamoDB import DynamoDB


class AppLambdaDelegate:
    def __init__(self, data: dict):
        self.data = data
        sts = STS().assume_role(
            base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
            "Ph-Back-RW"
        )
        self.dynamodb = DynamoDB(sts=sts)

    @property
    def dataset(self):
        return {
            "id": self.data.get("dataset_id"),
            "projectId": self.data.get("projectId"),
            "date": int(time.time()),
            "label": "[]",
            "name": self.data.get("name"),
            "schema": "[]",
            "version": self.data.get("version"),
            "cat": self.data.get("cat"),
            "path": self.data.get("message"),
            "format": self.data.get("format"),
            "prop": self.data.get("prop")
        }

    @property
    def notification(self):
        return {
            "id": self.data.get("id"),
            "projectId": self.data.get("projectId"),
            "category": self.data.get("category"),
            "code": self.data.get("code"),
            "comments": self.data.get("comments"),
            "date": int(time.time()),
            "jobCat": self.data.get("jobCat"),
            "jobDesc": self.data.get("jobDesc"),
            "message": self.data.get("message"),
            "owner": self.data.get("owner"),
            "showName": self.data.get("showName"),
        }

    @property
    def dag(self):
        return {
            "projectId": self.data.get("projectId"),
            "sortVersion": "developer_" + self.data.get("dataset_id"),
            "ctype": "node",
            "cat": "dataset",
            "level": "-99999",
            "runtime": self.data.get("cat"),
            "cmessage": "",
            "flowVersion": "developer",
            "name": self.data.get("name"),
            "position": '{"x": "0", "y": "0", "z": "0", "w": "0", "h": "0"}',
            "prop": self.data.get("prop"),
            "representId": self.data.get("dataset_id"),
        }

    def run(self):
        # try:
        self.dynamodb.putData({"table_name": "dataset", "item": self.dataset})
        print(self.dataset)
        print(self.notification)
        self.dynamodb.putData({"table_name": "notification", "item": self.notification})
        print(1111)
        self.dynamodb.putData({"table_name": "dag", "item": self.dag})
        print(222222)
        #     return True
        # except:
        #     return False


def lambda_handler(event, context):
    records = event["Records"]
    # try:
    for record in records:
        if record["eventName"].lower() != "insert":
            continue

        new_image = record["dynamodb"]["NewImage"]
        jobCat = new_image.get("jobCat", {"S": "None"})["S"]
        if record["eventName"].lower() == "insert" and (jobCat == "max1.0" or jobCat == "catalog"):

            data = {
                "id": new_image.get("id")["S"],
                "dataset_id": json.loads(new_image.get("message")["S"]).get('id'),
                "projectId": new_image.get("projectId")["S"],
                "category": "",
                "code": 0,
                "comments": "",
                "jobCat": "max1.0",
                "jobDesc": new_image.get("jobDesc")["S"],
                "message": json.loads(new_image.get("message")["S"]).get('keys'),
                "owner": new_image.get("owner")["S"],
                "showName": new_image.get("showName")["S"],
                "name": json.loads(new_image.get("message")["S"]).get('name'),
                "version": json.loads(new_image.get("message")["S"]).get('version'),
                "cat": json.loads(new_image.get("message")["S"]).get('cat'),
                "format": json.loads(new_image.get("message")["S"]).get('format'),
                "prop": json.dumps(json.loads(new_image.get("message")["S"]).get('prop', {}))
            }
            print(json.loads(new_image.get("message")["S"]))
            print(type(json.loads(new_image.get("message")["S"]).get('prop', '')))
            print(data)
            print(type(data['dataset_id']))
            app = AppLambdaDelegate(data)
            app.run()
    return True
    # except:
    #     return False
