import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
这个函数只做一件事情，将 scenario steps 的所有东西写到 scenario_step dynamodb中
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
        "steps": [
            {
                "confData": {},
                "detail": {
                    "type":"dataset",
                    "recursive":false,
                    "ignore-error":false,
                    "name":"1235"
                },
                "index": 0,
                "mode": "dataset",
                "name": "alfred",
                "id": "step id",
            }
        ]
    }

return = {
    "steps": [
        {
            "confData": {},
            "detail": {
                "type":"dataset",
                "recursive":false,
                "ignore-error":false,
                "name":"1235"
            },
            "index": 0,
            "mode": "dataset",
            "name": "alfred",
            "id": "step id",
            "oldImage": {
                "confData": {},
                "detail": {
                    "type":"dataset",
                    "recursive":false,
                    "ignore-error":false,
                    "name":"1235"
                },
                "index": 0,
                "mode": "dataset",
                "name": "alfred",
                "id": "step id",
            }
        }
    ]
}
'''
class StepsIndex:
    def __init__(self, event):
        self.event = event
        self.steps = event['steps'] if len(event['steps']) == 0 else event['steps'][0]

    def get_scenarioId(self):
        return self.event['scenario']['id']

    def get_id(self):
        return self.steps['id']

    def get_confData(self):
        return self.steps['confData']

    def get_detail(self):
        return self.steps['detail']

    def get_index(self):
        return self.steps['index']

    def get_mode(self):
        return self.steps['mode']

    def get_name(self):
        return self.steps['name']

    def get_traceId(self):
        return self.event['traceId']

    def dumps_data_by_json(self, data):
        if isinstance(data, str):
            return data
        else:
            return json.dumps(data)

    def put_item(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scenario_step')
        response = table.put_item(
            Item={
                'scenarioId': self.get_scenarioId(),
                'id': self.get_id(),
                'confData': self.get_confData(),
                'detail': self.dumps_data_by_json(self.get_detail()),
                'index': self.get_index(),
                'mode': self.get_mode(),
                'name': self.get_name(),
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

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data

    def get_OldImage(self):
        Items= self.query_table_item('scenario_step', 'scenarioId', 'id')
        print("*"*50+"step content"+"*"*50)
        print(Items)
        if len(Items) != 0:
            ItemDict = Items[0]
            OldImage = {
                "confData": ItemDict['confData'],
                "detail": ItemDict['detail'],
                "index": self.turn_decimal_into_int(ItemDict['index']),
                "mode": ItemDict['mode'],
                "name": ItemDict['name'],
                "id": ItemDict['id']
            }
        else:
            OldImage = {}
        self.OldImage = OldImage
        return OldImage

    def fetch_result(self):
        if len(self.steps) == 0:
            return self.steps
        else:
            self.steps['OldImage'] = self.OldImage
            return [self.steps]


def lambda_handler(event, context):

    StepsClient = StepsIndex(event)
    if len(StepsClient.steps) == 0:
        pass
    else:
        StepsClient.get_OldImage()
        StepsClient.put_item()

    #return StepsClient.fetch_result()
    return {"type": "notification", "opname": event['owner'],
            "cnotification": {"data": {"datasets": [StepsClient.fetch_result()]}, "error": ''}}