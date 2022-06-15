import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from datetime import datetime
from decimal import Decimal

'''
删除steps里面的东西

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": "$.scenario",
        "steps.$": "$.steps"
    }
'''

class DelStepsIndex:

    def __init__(self, event):
        self.event = event
        self.steps = event['steps']

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


    def del_table_item(self, tableName, **kwargs):

        DelItem = dict(kwargs.items())
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        table.delete_item(
            Key=DelItem,
        )

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data

    def get_OldImage(self, ItemDict):
        if len(ItemDict) != 0:
            OldImage = {
                "confData": ItemDict['confData'],
                "detail": ItemDict['detail'],
                "index": self.turn_decimal_into_int(ItemDict['index']),
                "mode": ItemDict['mode'],
                "name": ItemDict['name'],
                "id": ItemDict['id'],
                "scenarioId": ItemDict["scenarioId"]
            }
        else:
            OldImage = {}
        return OldImage

    def DelStepItemFromDyDB(self):

        for step in self.steps:
            stepId = step["id"]
            scenarioId = step["scenarioId"]
            #----------per oldImageItem of step -----------------#
            OldImageItem = self.query_table_item('scenario_step', scenarioId=scenarioId, id=stepId)
            OldImage = self.get_OldImage(OldImageItem)
            #---------- item not exist --------------------------#
            if len(OldImage) == 0:
                pass
            else:
                #--------delete step item ------------------------#
                self.del_table_item('scenario_step', scenarioId=scenarioId, id=stepId)
            step['OldImage'] = OldImage

        return self.steps


def lambda_handler(event, context):

        DelClient = DelStepsIndex(event)

        #----- delete each step in array of steps -----------#
        result = DelClient.DelStepItemFromDyDB()

        return result
