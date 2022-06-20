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
        self.scenario = event["scenario"]
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

    def DelStepItemFromDyDB(self, tableName, stepsItems):

        for step in stepsItems:
            stepId = step["id"]
            scenarioId = step["scenarioId"]
            #----------per oldImageItem of step -----------------#
            OldImageItem = self.query_table_item(tableName, scenarioId=scenarioId, id=stepId)
            OldImage = self.get_OldImage(OldImageItem)
            #---------- item not exist --------------------------#
            if len(OldImage) == 0:
                pass
            else:
                #--------delete step item ------------------------#
                self.del_table_item(tableName, scenarioId=scenarioId, id=stepId)
            step['OldImage'] = OldImage

        return stepsItems


        #--将嵌套的list结构摊平---#
    def Flatten_Data_Of_List(self, Structure_list):
        from itertools import chain
        return list(chain(* Structure_list))

    def DelAllScenarioTriggesOrSingleScenarioTrigger(self):

        del_steps_list = []
        if len(self.scenario) == 0:
            del_steps_list = self.DelStepItemFromDyDB("scenario_step", self.steps)
        else:
            for each_scenario in self.scenario:
                each_array_step = each_scenario["steps"]
                each_del_list = self.DelStepItemFromDyDB("scenario_step", each_array_step)
                del_steps_list.append(each_del_list)
            del_steps_list = self.Flatten_Data_Of_List(del_steps_list)
        return del_steps_list


def lambda_handler(event, context):

        DelClient = DelStepsIndex(event)

        #----- delete each step in array of steps -----------#
        result = DelClient.DelAllScenarioTriggesOrSingleScenarioTrigger()

        return result
