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

    def query_table_item(self, tableName, **kwargs):
        QueryItem = dict(kwargs.items())
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.get_item(
            Key=QueryItem,
        )
        try:
            Item = res["Item"]
        except:
            Item = []
        return Item

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data

    def get_OldImage(self, ItemDict):
        if len(ItemDict) != 0:
            OldImage = {
                "id": ItemDict['id'],
                "active": ItemDict['active'],
                "scenarioName": ItemDict['scenarioName'],
                "index": self.turn_decimal_into_int(ItemDict['index'])
            }
        else:
            OldImage = {}
        return OldImage

    def DelScenarioItemFromDyDB(self):

        for scenario in self.scenario:
            ScenarioId = scenario["id"]
            OldImageItem = self.query_table_item("scenario", projectId=self.get_projectId(), id=ScenarioId)
            OldImage = self.get_OldImage(OldImageItem)
            if len(OldImage) == 0:
                pass
            else:
                #--------deleter scenario items -----------#
                self.del_table_item("scenario", projectId=self.get_projectId(), id=ScenarioId)
            scenario["OldImage"] = OldImage
        return self.scenario


def lambda_handler(event, context):

    DelClient = DelScenarioIndex(event)
    #-------------------delete ---------------------------------------------#
    result = DelClient.DelScenarioItemFromDyDB()

    return result


