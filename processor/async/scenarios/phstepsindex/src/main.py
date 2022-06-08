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
        self.steps = event['steps']

    def get_scenarioId(self):
        return self.event['scenario']['id']

    def get_traceId(self):
        return self.event['traceId']

    def dumps_data_by_json(self, data):
        if isinstance(data, str):
            return data
        else:
            return json.dumps(data)

    def put_item(self, scenarioId, stepID, confData, detail, index, mode, name, traceId):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scenario_step')
        response = table.put_item(
            Item={
                'scenarioId': scenarioId,
                'id': stepID,
                'confData': confData,
                'detail': self.dumps_data_by_json(detail),
                'index': index,
                'mode': mode,
                'name': name,
                'traceId': traceId
            }
        )
        return response

    def query_table_item(self, tableName, partitionKey, sortKey, stepId):
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(self.get_scenarioId())
                                   & Key(sortKey).eq(stepId)
        )
        return res["Items"]

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data

    def get_OldImage(self, stepId):
        Items= self.query_table_item('scenario_step', 'scenarioId', 'id', stepId)
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
        return OldImage


    def putStepItemIntoDyDB(self):
        for step in self.steps:
            stepID = step["id"]
            detail = step["detail"]
            confData = step["confData"]
            index = step["index"]
            mode = step["mode"]
            name = step["name"]
            #-------- get oldImage -------------------------#
            oldImage = self.get_OldImage(stepID)
            step["OldImage"] = oldImage
            #-------- put step item int dyDB-----------------#
            self.put_item(self.get_scenarioId(), stepID, confData, detail, index, mode, name, self.get_traceId())
        return self.steps


def lambda_handler(event, context):

    StepsClient = StepsIndex(event)

    result = StepsClient.putStepItemIntoDyDB()

    return result