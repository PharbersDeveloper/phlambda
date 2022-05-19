import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime

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
        self.trigger = event['triggers'][0]
        self.step = event['steps'][0]
        self.errorMessage = {}

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

    def get_OldImage(self):
        pass

    def IsTheSameItem(self):
        pass

    def scenarioRollBack(self):
        pass

    def triggerRollBack(self):
        pass

    def stepRollBack(self):
        pass

def lambda_handler(event, context):

    #---------------------回滚操作--------------------------------#
    delClient = DelRollBack(event)
    #TODO 回滚scenario时，需同时回滚子级层次的trigger 和step 数据,现在暂时没确定scenario里的oldimage数据结构，后面对接时候再做
    #------------------------- scenario -------------------------#
    #delClient.scenarioRollBack()
    delClient.triggerRollBack()
    delClient.stepRollBack()

    return True
