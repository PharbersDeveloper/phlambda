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

    def get_triggerId(self):
        return self.triggers['id']

    def query_table_item(self, tableName, **kwargs):
        QueryItem = dict(kwargs.items())
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            Key=QueryItem,
        )
        return res["Items"]


    def del_table_item(self, tableName, **kwargs):

        DelItem = dict(kwargs.items())
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        table.delete_item(
            Key=DelItem,
        )

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data

    def get_OldImage(self, Items):
        if len(Items) != 0:
            ItemDict = Items[0]
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

    def fetch_result(self):
        self.triggers['OldImage'] = self.OldImage
        return self.OldImage


def lambda_handler(event, context):

    DelClient = DeltriggerIndex(event)
    #--------------------------get OldImage-------------------------------------------------------#
    OldImageItem = DelClient.query_table_item('scenario_trigger', scenarioId=DelClient.get_scenarioId(), id=DelClient.get_triggerId())
    OldImage = DelClient.get_OldImage(OldImageItem)
    if len(OldImage) == 0:
        print(f"triggersId :{DelClient.get_triggerId()} not exits, please check data")
    else:
        #-------------------------delete trigger----------------------------------------------------------#
        DelClient.del_table_item('scenario_trigger', scenarioId=DelClient.get_scenarioId(), id=DelClient.get_triggerId())

    return DelClient.fetch_result()
