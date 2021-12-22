
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

    def query_version(self, project_id, **kwargs):
        result = self.dynamodb.queryTable({
            "table_name": "version",
            "expression": Key('project_id').eq(f'{project_id}')
        })
        if result:
            result[0]['updatetime'] = int(result[0]['updatetime'])
            return result[0]


def lambda_handler(event, context):
    try:
        if event.get('jobCat') != 'max1.0':
            return {
                "statusCode": 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                "body": json.dumps({"message": "jobCat != max1.0"})
            }
        app = AppLambdaDelegate(event)
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": app.run()})
        }

    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e)})
        }
