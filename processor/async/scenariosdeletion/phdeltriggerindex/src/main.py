import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from datetime import datetime
from decimal import Decimal

'''
删除triggerindex里面的东西

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": "$.scenario",
        "triggers.$": "$.triggers"
    }
'''

class DeltriggerIndex:

    def __init__(self, event):
        self.event = event
        self.triggers = event['triggers']

    def get_scenarioId(self):
        return self.event['scenario']['id']

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
                "active": ItemDict['active'],
                "detail": ItemDict['detail'],
                "index": self.turn_decimal_into_int(ItemDict['index']),
                "mode": ItemDict['mode'],
                "id": ItemDict['id']
            }
        else:
            OldImage = {}
        self.OldImage = OldImage
        return OldImage

    def DeltriggerItemFromDyDB(self):

        for trigger in self.triggers:
            triggerId = trigger["id"]
            #--------each oldImageItem of trigger -----------#
            OldImageItem = self.query_table_item('scenario_trigger', scenarioId=self.get_scenarioId(), id=triggerId)
            OldImage = self.get_OldImage(OldImageItem)
            #-------- item not exist ------------------------#
            if len(OldImage) == 0:
                pass
            else:
                #------delete trigger item ------------------#
                self.del_table_item('scenario_trigger', scenarioId=self.get_scenarioId(), id=triggerId)
            trigger["OldImage"] = OldImage

        return self.triggers


def lambda_handler(event, context):

       DelClient = DeltriggerIndex(event)

       #-------------- delete each trigger in array of triggers ------------#
       result = DelClient.DeltriggerItemFromDyDB()

       return result
