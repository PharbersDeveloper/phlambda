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

class DelReportsIndex:

    def __init__(self, event):
        self.event = event
        self.scenario = event["scenario"]
        self.reports = event['reports']

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
                "name": ItemDict['name'],
                "id": ItemDict['id'],
                "scenarioId": ItemDict["scenarioId"],
                "traceId": ItemDict["traceId"]
            }
        else:
            OldImage = {}
        return OldImage

    def DelReportItemFromDyDB(self, tableName, reportsItems):

        for report in reportsItems:
            reportId = report["id"]
            scenarioId = report["scenarioId"]
            #----------per oldImageItem of step -----------------#
            OldImageItem = self.query_table_item(tableName, scenarioId=scenarioId, id=reportId)
            OldImage = self.get_OldImage(OldImageItem)
            #---------- item not exist --------------------------#
            if len(OldImage) == 0:
                pass
            else:
                #--------delete step item ------------------------#
                self.del_table_item(tableName, scenarioId=scenarioId, id=reportId)
            report['OldImage'] = OldImage

        return reportsItems


        #--将嵌套的list结构摊平---#
    def Flatten_Data_Of_List(self, Structure_list):
        from itertools import chain
        return list(chain(* Structure_list))

    def DelAllScenarioTriggesOrSingleScenarioTrigger(self):

        del_reports_list = []
        if len(self.scenario) == 0:
            del_reports_list = self.DelReportItemFromDyDB("scenario_report", self.reports)
        else:
            for each_scenario in self.scenario:
                each_array_report = each_scenario["reports"]
                each_del_list = self.DelReportItemFromDyDB("scenario_report", each_array_report)
                del_reports_list.append(each_del_list)
            del_reports_list = self.Flatten_Data_Of_List(del_reports_list)
        return del_reports_list


def lambda_handler(event, context):

        DelClient = DelReportsIndex(event)

        #----- delete each step in array of steps -----------#
        result = DelClient.DelAllScenarioTriggesOrSingleScenarioTrigger()

        return result
