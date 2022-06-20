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
        self.scenario = event["scenario"]
        self.triggers = event['triggers']

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
                "id": ItemDict['id'],
                "scenarioId": ItemDict["scenarioId"]
            }
        else:
            OldImage = {}
        return OldImage

    def DeltriggerItemFromDyDB(self, tableName, triggersItems):

        for trigger in triggersItems:
            triggerId = trigger["id"]
            scenarioId = trigger["scenarioId"]
            #--------each oldImageItem of trigger -----------#
            OldImageItem = self.query_table_item(tableName, scenarioId=scenarioId, id=triggerId)
            OldImage = self.get_OldImage(OldImageItem)
            #-------- item not exist ------------------------#
            if len(OldImage) == 0:
                pass
            else:
                #------delete trigger item ------------------#
                self.del_table_item(tableName, scenarioId=scenarioId, id=triggerId)
            trigger["OldImage"] = OldImage

        return triggersItems

    #--将嵌套的list结构摊平---#
    def Flatten_Data_Of_List(self, Structure_list):
        from itertools import chain
        return list(chain(* Structure_list))

    def DelAllScenarioTriggesOrSingleScenarioTrigger(self):

        del_triggers_list = []
        if len(self.scenario) == 0:
            del_triggers_list = self.DeltriggerItemFromDyDB("scenario_triggers", self.triggers)
        else:
            for each_scenario in self.scenario:
                each_array_trigger = each_scenario["triggers"]
                each_del_list = self.DeltriggerItemFromDyDB("scenario_triggers", each_array_trigger)
                del_triggers_list.append(each_del_list)
            del_triggers_list = self.Flatten_Data_Of_List(del_triggers_list)
        return del_triggers_list

def lambda_handler(event, context):

       DelClient = DeltriggerIndex(event)

       #-------------- delete each trigger in array of triggers ------------#
       del_triggers_list = DelClient.DelAllScenarioTriggesOrSingleScenarioTrigger()

       return del_triggers_list
