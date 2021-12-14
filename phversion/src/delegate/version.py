import os
import json
import time
import base64
from util.AWS.STS import STS
from constants.Common import Common
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Attr, Key


class AppLambdaDelegate:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        sts = STS().assume_role(
            base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
            "Ph-Back-RW"
        )
        self.dynamodb = DynamoDB(sts=sts)

    def inster_version(self, **kwargs):
        item = self.parse_data(kwargs)
        if self.query_version(item['project_id']):
            return 'project_id alrady exist'
        self.dynamodb.putData({"table_name": "version", "item": item})
        return 'insert data succeed'

    def query_version(self, project_id, **kwargs):
        return self.dynamodb.queryTable({
            "table_name": "version",
            "expression": Key('project_id').eq(f'{project_id}')
        })

    def querytime_version(self, **kwargs):
        return self.dynamodb.scanTable({
            "table_name": "version",
            "expression": Attr('updatetime').lt(int(time.time()))
        })

    def parse_data(self, item):
        item['sort_key'] = item['name'] + item['version_msg']
        item['updatetime'] = int(time.time())
        return item

    def run(self):
        Commends = {
            "insert_item": self.inster_version,
            "query_data": self.query_version,
            "query_time": self.querytime_version,
        }
        body = eval(self.event["body"])
        action = body.pop('action')
        return Commends[action](**body)



#
# sts = STS().assume_role(
#     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
#     "Ph-Back-RW"
# )
# dynamodb = DynamoDB(sts=sts)
# table = dynamodb.dynamodb_resource.Table('version')
# print(table.scan(
#         FilterExpression=Attr('updatetime').lt(int(time.time()))
# )["Items"])
#
# print(table.scan(
#         FilterExpression=Key('project_id').eq('002')
# ))
