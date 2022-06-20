import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime
from decimal import Decimal

'''
删除失败后将所有的东西写回到数据库中，
在写之前判断是否存在并且判断是否相同

args:
    event = {
        "common": {
            "traceId": "alfred-resource-creation-traceId",
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred"
        },
        "action": {
            "cat": "createOrUpdateScenario",
            "desc": "create or update scenario",
            "comments": "something need to say",
            "message": "something need to say",
            "required": true
        },
        "notification": {
            "required": true      
        },
        "scenario": {
            "id": "scenario id",       # 如果有就是update，如果没有就是新建
            "active": true,
            "scenarioName": "scenario name",
            "deletion": true | false      # 如果是true，则所有和scenario相关的全部删除
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
                "id": "trigger id",       # 如果有就是update，如果没有就是新建
            }
        ],
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
                "mode": "dataset",,
                "name": "alfred"
                "id": "step id",       # 如果有就是update，如果没有就是新建
            }
        ],
        "error": {
            "Error": "Exception",
            "Cause": ""
        }
    }
'''


class DelRollBack:
    def __init__(self, event):
        self.event = event
        self.scenario = event['scenario']
        self.triggers = event['triggers']
        self.steps = event['steps']

    def get_projectId(self):
        return self.event['common']['projectId']

    def get_traceId(self):
        return self.event['common']['traceId']

    def get_owner(self):
        return self.event['common']['owner']

    def get_projectName(self):
        return self.event['common']['projectName']

    def get_scenarioName(self):
        return self.scenario["scenarioName"]

    def check_OldImage(self, mode_type):
        try:
            return "NotNeedRollBack" if len(mode_type['OldImage']) == 0 else "RollBack"
        except Exception as e:
            print("*"*50+"OldImage ERROR"+"*"*50 + "\n", str(e))
            return "NotNeedRollBack"

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data


    def get_scenarioItem(self, OldImage):
        scenarioItem = {
            'projectId': self.get_projectId(),
            'id': OldImage['id'],
            'active': OldImage['active'],
            'args': '',
            'index': self.turn_decimal_into_int(OldImage['index']),
            'owner': self.get_owner(),
            'projectName': self.get_projectName(),
            'scenarioName': OldImage['scenarioName'],
            'traceId': self.get_traceId()
        }
        return scenarioItem

    def get_triggerItem(self, OldImage):
        trigger_Item = {
            'scenarioId': OldImage["scenarioId"],
            'id': OldImage['id'],
            'active': OldImage['active'],
            'detail': OldImage['detail'],
            'index': self.turn_decimal_into_int(OldImage['index']),
            'mode': OldImage['mode'],
            'traceId': OldImage["traceId"]
        }
        return trigger_Item

    def get_stepItem(self, OldImage):
        step_Item = {
            'scenarioId': OldImage["scenarioId"],
            'id': OldImage['id'],
            'confData': OldImage['confData'],
            'detail': OldImage['detail'],
            'index': self.turn_decimal_into_int(OldImage['index']),
            'mode': OldImage['mode'],
            'name': OldImage['name'],
            'traceId': OldImage["traceId"]
        }
        return step_Item

    def query_table_item(self, tableName, **kwargs):
        QueryItem = dict(kwargs.items())
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            Key=QueryItem,
        )
        try:
            item = res["Items"]
        except:
            item = []
        return item

    def map_Item(self, tableName, OldImage):
        tableMap = {
            "scenario": self.get_scenarioItem,
            "scenario_trigger": self.get_triggerItem,
            "scenario_step": self.get_stepItem
        }
        return tableMap[tableName](OldImage)

    def put_item(self, tableName, Item):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        response = table.put_item(
            Item=Item
        )
        return response

    #-------------------检查Item是否一致----------------------------#
    def IsTheSameItem(self, OldItem, CurrentItem):

        return True if OldItem == CurrentItem else False

    def RollBackProcess(self, modeType, tableName, **kwargs):
        QueryConditionDict = dict(kwargs.items())
        oldImage = self.get_OldImage(modeType)
        Item = self.map_Item(tableName, oldImage)
        #--------------检查item是否一致-------------------------------#
        queryTableItem = self.query_table_item(tableName, **(QueryConditionDict))
        if len(queryTableItem) == 0:
            self.put_item(tableName, Item)
        else:
            if self.IsTheSameItem(Item, self.map_Item(tableName, queryTableItem)):
                self.NotNeedRollBack()
            else: #----覆盖操作-----------------#
                self.put_item(tableName, Item)


    def NotNeedRollBack(self):
        print("not neet RollBack...")

    def get_OldImage(self, modeType):
        return modeType['OldImage']

    def scenarioRollBack(self):
        SceanrioNum = 0
        ScenarioRollBackResult = []

        for scenario in self.scenario:
            ScenarioId = scenario["id"]

            scenarioRollBackMessage = {}
            scenarioRollBackMessage["index"] = SceanrioNum + 1
            RollBackMode = self.check_OldImage(self.scenario)

            if RollBackMode == "RollBack":
                self.RollBackProcess(self.scenario, "scenario", **{"projectId": self.get_projectId(), "id": ScenarioId})
            else:
                self.NotNeedRollBack()
            scenarioRollBackMessage["name"] = self.get_scenarioName()
            scenarioRollBackMessage["mode"] = f"error handle mode: {RollBackMode}"

            ScenarioRollBackResult.append(scenarioRollBackMessage)
        return ScenarioRollBackResult


    def triggerRollBack(self):
        triggerCountNum = 0
        triggerRollBackResult = []

        for trigger in self.triggers:
            triggerId = trigger["id"]
            scenarioId = trigger["scenarioId"]
            #-------- rollback message --------------------#
            eachRollBackMessage = {}
            eachRollBackMessage["index"] = triggerCountNum + 1
            eachRollBackMessage["name"] = trigger["name"]
            RollBackMode = self.check_OldImage(trigger)
            eachRollBackMessage["mode"] = f" error handle mode: {RollBackMode}"
            #-------- rollback message --------------------#

            if RollBackMode == "RollBack":
                self.RollBackProcess(trigger, "scenario_trigger", **{"scenarioId": scenarioId, "id": triggerId})
            else:
                self.NotNeedRollBack()
            triggerRollBackResult.append(eachRollBackMessage)

        return triggerRollBackResult

    def stepRollBack(self):

        stepCountNum = 0
        StepRollBackResult = []
        for step in self.steps:
            eachRollBackMessage = {}
            stepId = step["id"]
            scenarioId = step["scenarioId"]
            #-------- rollback message --------------------#
            eachRollBackMessage["index"] = stepCountNum + 1
            eachRollBackMessage["name"] = step["name"]
            RollBackMode = self.check_OldImage(step)
            eachRollBackMessage["mode"] = f" error handle mode: {RollBackMode}"
            #-------- rollback message --------------------#

            if RollBackMode == "RollBack":
                self.RollBackProcess(step, "scenario_step", **{"scenarioId": scenarioId, "id": stepId})
            else:
                self.NotNeedRollBack()
            StepRollBackResult.append(eachRollBackMessage)
        return StepRollBackResult

    def fetch_result(self, scenarioRollBackResult, triggerRollBackResult, StepRollBackResult):
        errorMessage = {
            "scenario": scenarioRollBackResult,
            "triggers": triggerRollBackResult,
            "steps": StepRollBackResult
        }

        return {"type": "notification", "opname": self.get_owner(),
                "cnotification": {"data": {"datasets": []}, "error": errorMessage}}


def lambda_handler(event, context):

    #---------------------回滚操作--------------------------------#
    try:
        delClient = DelRollBack(event)
        scenarioRollBackResult = delClient.scenarioRollBack()
        triggerRollBackResult  = delClient.triggerRollBack()
        StepRollBackResult = delClient.stepRollBack()
        return delClient.fetch_result(scenarioRollBackResult, triggerRollBackResult, StepRollBackResult)
    except Exception as e:
        try:
            opname = event["common"]["owner"]
        except:
            opname = "unknown"
        return {"type": "notification", "opname": opname,
         "cnotification": {"data": {"datasets": []}, "error": str(e)}}

