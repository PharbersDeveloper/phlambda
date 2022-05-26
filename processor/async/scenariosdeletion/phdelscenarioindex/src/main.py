import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from datetime import datetime
from decimal import Decimal



'''
删除 scenario 里面的东西

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": "$.scenario"
    }
'''

class DelScenarioIndex:

    def __init__(self, event):
        self.event = event
        self.scenario = event['scenario']

    def get_projectId(self):
        return self.event['projectId']

    def get_scenarioId(self):
        return self.scenario['id']

    def del_table_item(self, tableName, **kwargs):

        DelItem = dict(kwargs.items())
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        table.delete_item(
            Key=DelItem,
        )

    def query_table_item(self, tableName, partitionKey, sortKey):
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(self.get_projectId())
                               & Key(sortKey).eq(self.get_scenarioId())
        )
        return res["Items"]


    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data

    def get_OldImage(self):
        Items= self.query_table_item('scenario', 'projectId', 'id')
        print("*"*50+"OldImage contents"+"*"*50)
        print(Items)
        if len(Items) != 0:
            ItemDict = Items[0]
            OldImage = {
                "id": ItemDict['id'],
                "active": ItemDict['active'],
                "scenarioName": ItemDict['scenarioName'],
                "index": self.turn_decimal_into_int(ItemDict['index'])
            }
        else:
            OldImage = {}
        self.OldImage = OldImage
        return OldImage

    def fetch_result(self):
        self.scenario['OldImage'] = self.OldImage
        return self.scenario


def lambda_handler(event, context):

    DelClient = DelScenarioIndex(event)

    #-------------------delete step---------------------------------------------#
    OldImage = DelClient.get_OldImage()
    if len(OldImage) == 0:
        print(f"{DelClient.get_scenarioId()} not exits, please check data")
    else:
        #-------------------delete scenario---------------------------------------------#
        DelClient.del_table_item('scenario', projectId=DelClient.get_projectId(), id=DelClient.get_scenarioId())

    return DelClient.fetch_result()


