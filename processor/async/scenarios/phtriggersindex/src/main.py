import json
import boto3
from boto3.dynamodb.conditions import Attr,Key

'''
这个函数只做一件事情，将 trigger 的所有东西写到 scenario_trigger dynamodb中
args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": {
            "id": "scenario id",
            "active": true,
            "scenarioName": "scenario name",
            "deletion": false
        },
        "triggers": [
            {
                "active": true,
                "detail": {
                    "timezone":"中国北京",
                    "start":"2022-04-26 16:10:14",
                    "period":"minute",
                    "value":1
                },
                "index": 0,
                "mode": "timer",
                "id": "trigger id"
            }
        ]
    }
'''
class TriggersIndex:
    def __init__(self, event):
        self.event = event
        self.triggers = self.event['triggers'][0]

    def get_scenarioId(self):
        return self.event['scenario']['id']
    def get_id(self):
        return self.triggers['id']
    def get_active(self):
        return self.triggers['active']
    def get_detail(self):
        return self.triggers['detail']
    def get_index(self):
        return self.triggers['index']
    def get_mode(self):
        return self.triggers['mode']
    def get_traceId(self):
        return self.event['traceId']

    def put_item(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scenario_trigger')
        response = table.put_item(
            Item={
                'scenarioId': self.get_scenarioId(),
                'id': self.get_id(),
                'active': self.get_active(),
                'detail': self.get_detail(),
                'index': self.get_index(),
                'mode': self.get_mode(),
                'traceId': self.get_traceId()
            }
        )
        return response

    def query_table_item(self, tableName, partitionKey, sortKey):
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(self.get_scenarioId())
                                   & Key(sortKey).eq(self.get_id())
        )
        return res["Items"]

    def get_OldImage(self):
        Items= self.query_table_item('scenario_trigger', 'scenarioId', 'id')
        if Items[0]:
            OldImage = {
                "active": Items['active'],
                "detail": Items['detail'],
                "index": Items['index'],
                "mode": Items['mode'],
                "id": Items['id']
            }
        else:
            OldImage = {}
        self.OldImage = OldImage
        return OldImage

    def fetch_result(self):
        self.triggers['OldImage'] = self.OldImage
        return [self.triggers]

def lambda_handler(event, context):

    triggersClient = TriggersIndex(event)
    triggersClient.get_OldImage()
    triggersClient.put_item()

    return triggersClient.fetch_result()