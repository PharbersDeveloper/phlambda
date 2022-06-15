import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

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
        self.triggers = event['triggers']

    def get_traceId(self):
        return self.event['traceId']

    def put_item(self, scenarioId, TriggerId, active, detail, index, mode, traceId):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scenario_trigger')
        response = table.put_item(
            Item={
                'scenarioId': scenarioId,
                'id': TriggerId,
                'active': active,
                'detail': self.dumps_data_by_json(detail),
                'index': index,
                'mode': mode,
                'traceId': traceId
            }
        )
        return response

    def query_table_item(self, tableName, partitionKey, sortKey, scenarioId, TriggerId):
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(scenarioId)
                                   & Key(sortKey).eq(TriggerId)
        )
        return res["Items"]

    def dumps_data_by_json(self, data):
        if isinstance(data, str):
            return data
        else:
            return json.dumps(data)

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data


    def get_OldImage(self, scenarioId, TriggerId):
        Items= self.query_table_item('scenario_trigger', 'scenarioId', 'id', scenarioId, TriggerId)
        print("*"*50+"trigger content " + "*"*50)
        print(Items)
        if len(Items) != 0:
            ItemDict = Items[0]
            OldImage = {
                "active": ItemDict['active'],
                "detail": ItemDict['detail'],
                "index": self.turn_decimal_into_int(ItemDict['index']),
                "mode": ItemDict['mode'],
                "id": ItemDict['id'],
                "scenarioId": ItemDict["scenarioId"]
            }
        else:
            OldImage = {}
        return OldImage


    def putTriggersItemIntoDyDB(self):
        for trigger in self.triggers:
            triggerId = trigger["id"]
            scenarioId = trigger["scenarioId"]
            detail = trigger["detail"]
            active = trigger["active"]
            index = trigger["index"]
            mode = trigger["mode"]
            #-------- get oldImage -------------------------#
            oldImage = self.get_OldImage(scenarioId, triggerId)
            trigger["OldImage"] = oldImage
            #-------- put Trigger item int dyDB-----------------#
            self.put_item(scenarioId, triggerId, active, detail, index, mode, self.get_traceId())
        return self.triggers

def lambda_handler(event, context):

    triggersClient = TriggersIndex(event)

    result = triggersClient.putTriggersItemIntoDyDB()

    return result