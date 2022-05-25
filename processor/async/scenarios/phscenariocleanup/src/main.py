import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from datetime import datetime

'''
这个函数只做两件事情，
# 1. 将所有的错误都提取出来写入到notification中
2. 将创建成功但整体失败的东西会滚

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

class RollBack:
    def __init__(self, event):
        self.event = event
        self.scenario = event['scenario']
        self.trigger = event['triggers'][0]
        self.step = event['steps'][0]
        self.errorMessage = {}
        print("*"*50+"event"+"*"*50)
        print(self.event)

    def get_projectId(self):
        return self.event['common']['projectId']

    def get_scenarioId(self):
        return self.scenario['id']

    def get_stepId(self):
        return self.step['id']

    def get_triggerId(self):
        return self.trigger['id']

    def get_traceId(self):
        return self.event['common']['traceId']

    def get_owner(self):
        return self.event['common']['owner']

    def get_projectName(self):
        return self.event['common']['projectName']

    def check_OldImage(self, mode_type):
        try:
            return "Delete" if len(mode_type['OldImage']) == 0 else "RollBack"
        except Exception as e:
            print("*"*50+"OldImage ERROR"+"*"*50 + "\n", str(e))
            return "NotNeedRollBack"

    def get_OldImage(self, mode_type):
        return mode_type['OldImage']

    def get_scenarioItem(self, OldImage):
        scenarioItem = {
            'projectId': self.get_projectId(),
            'id': OldImage['id'],
            'active': OldImage['active'],
            'args': '',
            'index': OldImage['index'],
            'owner': self.get_owner(),
            'projectName': self.get_projectName(),
            'scenarioName': OldImage['scenarioName'],
            'traceId': self.get_traceId()
        }
        return scenarioItem

    def get_triggerItem(self, OldImage):
        trigger_Item = {
            'scenarioId': self.get_scenarioId(),
            'id': OldImage['id'],
            'active': OldImage['active'],
            'detail': OldImage['detail'],
            'index': OldImage['index'],
            'mode': OldImage['mode'],
            'traceId': self.get_traceId()
        }
        return trigger_Item

    def get_stepItem(self, OldImage):
        step_Item = {
            'scenarioId': self.get_scenarioId(),
            'id': OldImage['id'],
            'confData': OldImage['confData'],
            'detail': OldImage['detail'],
            'index': OldImage['index'],
            'mode': OldImage['mode'],
            'name': OldImage['name'],
            'traceId': self.get_traceId()
        }
        return step_Item

    def put_item(self, tableName, Item):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        response = table.put_item(
                Item=Item
        )
        return response

    def map_Item(self, tableName, OldImage):
        tableMap = {
            "scenario": self.get_scenarioItem,
            "scenario_trigger": self.get_triggerItem,
            "scenario_step": self.get_stepItem
        }
        return tableMap[tableName](OldImage)
    def NotNeedRollBack(self):
        print("not need RollBack...")
        pass

    def map_handle_mode(self, handle_mode):
        RollBackMode = {
            "Delete": self.del_table_item,
            "RollBack": self.RollBackProcess,
            "NotNeedRollBack": self.NotNeedRollBack,
        }
        return RollBackMode[handle_mode]

    def RollBackProcess(self, mode_type, tableName):
        oldImage = self.get_OldImage(mode_type)
        Item = self.map_Item(tableName, oldImage)
        self.put_item(tableName, Item)

    def scenarioRollBack(self):
        RollBackMode = self.check_OldImage(self.scenario)
        print(f"Mode: {RollBackMode}")
        self.errorMessage['scenario'] = f"error handle mode: {RollBackMode}"
        if RollBackMode == "Delete":
            return self.map_handle_mode(RollBackMode)("scenario", "projectId", "id", self.get_scenarioId(), self.get_scenarioId())
        elif RollBackMode == "RollBack":
            return self.map_handle_mode(RollBackMode)(self.scenario, "scenario")
        else:
            return self.map_handle_mode(RollBackMode)()


    def triggerRollBack(self):
        RollBackMode = self.check_OldImage(self.trigger)
        print(f"Mode: {RollBackMode}")
        self.errorMessage['scenario_trigger'] = f"error handle mode: {RollBackMode}"
        if RollBackMode == "Delete":
            return self.map_handle_mode(RollBackMode)("scenario_trigger", "scenarioId", "id", self.get_scenarioId(), self.get_triggerId())
        elif RollBackMode == "RollBack":
            return self.map_handle_mode(RollBackMode)(self.trigger, "scenario_trigger")
        else:
            return self.map_handle_mode(RollBackMode)()

    def stepsRollBack(self):
        RollBackMode = self.check_OldImage(self.step)
        print(f"Mode: {RollBackMode}")
        self.errorMessage['scenario_step'] = f"error handle mode: {RollBackMode}"
        if RollBackMode == "Delete":
            return self.map_handle_mode(RollBackMode)("scenario_step", "scenarioId", "id", self.get_scenarioId(), self.get_stepId())
        elif RollBackMode == "RollBack":
            return self.map_handle_mode(RollBackMode)(self.trigger, "scenario_step")
        else:
            return self.map_handle_mode(RollBackMode)()


    def del_table_item(self, tableName, partitionKey, sortKey, partitionValue, sortValue):
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(tableName)
            table.delete_item(
                Key={
                    partitionKey: partitionValue,
                    sortKey: sortValue
                },
            )

    def fetch_result(self):
        return {"type": "notification", "opname": self.get_projectId(),
                "cnotification": {"data": {"datasets": []}, "error": self.errorMessage}}

def lambda_handler(event, context):

    #-------------------回滚操作-----------------------------------#
    rollBackClient = RollBack(event)
    rollBackClient.scenarioRollBack()
    rollBackClient.triggerRollBack()
    rollBackClient.stepsRollBack()

    return rollBackClient.fetch_result()