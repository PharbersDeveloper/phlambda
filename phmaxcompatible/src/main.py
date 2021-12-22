
import os
import json
import time
import base64
from util.AWS.STS import STS
from constants.Common import Common
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Attr, Key


class AppLambdaDelegate:
    def __init__(self, data: dict):
        self.data = data
        sts = STS().assume_role(
            base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
            "Ph-Back-RW"
        )
        self.dynamodb = DynamoDB(sts=sts)

    def run(self):
        try:
            self.dynamodb.putData({"table_name": "dataset", "item": self.dataset})
            self.dynamodb.putData({"table_name": "notification", "item": self.notification})
            return True
        except:
            return False

    @property
    def dataset(self):
        return {
            "id": self.data.get("id"),
            "projectId": self.data.get("projectId"),
            "date": int(time.time()),
            "label": self.data.get("message"),
            "name": self.data.get("name"),
            "version": self.data.get("version")
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


def lambda_handler(event, context):
    records = event["Records"]
    try:
        for record in records:
            if record["eventName"].lower() != "insert":
                continue

            new_image = record["dynamodb"]["NewImage"]
            if record["eventName"].lower() == "insert" and \
                    new_image.get("jobCat", {"S": "None"})["S"] == "max1.0":
                data = {
                    "id": "e0d24d609b7fbf5b84918ec7720feaef.xlsx",
                    "projectId": new_image.get("jobCat")["S"],
                    "category": "",
                    "code": 0,
                    "comments": "",
                    "jobCat": "max1.0",
                    "jobDesc": new_image.get("jobDesc")["S"],
                    "message": json.loads(new_image.get("message")["S"]).get('keys'),
                    "owner": new_image.get("owner")["S"],
                    "showName": new_image.get("showName")["S"],
                    "name": json.loads(new_image.get("message")["S"]).get('name'),
                    "version": json.loads(new_image.get("message")["S"]).get('version')
                }
                app = AppLambdaDelegate(data)
                app.run()

    except:
        pass
