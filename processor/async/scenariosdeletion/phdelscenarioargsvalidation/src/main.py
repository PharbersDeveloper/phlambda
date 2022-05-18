import json
import boto3
from boto3.dynamodb.conditions import Attr
'''
这个函数只做一件事情，检查参数是否合法
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
            "id": "scenario id",       
            "active": true,
            "scenarioName": "scenario name"
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
        ]
    }
'''

class CheckParameters:

    def __init__(self, event):
        self.event = event
        self.check_dict = {
            "common": self.check_common,
            "action": self.check_action,
            "notification": self.check_notificaton,
            "scenario": self.check_scenario,
            "triggers": self.check_triggers,
            "steps": self.check_steps,
        }

    def get_prefix_key(self):
        return list(self.event.keys())

    def check_key(self, key):
        return self.check_dict[key](key)

    def check_type(self, key, data_type):
        try:
            if isinstance(self.event[key], data_type) is False:
                raise Exception(f"type error: {key} is not belong {str(data_type)}")
        except Exception as e:
            raise e

    def check_common(self, key):
        self.check_type(key, dict)

    def check_action(self, key):
        self.check_type(key, dict)

    def check_notificaton(self, key):
        self.check_type(key, dict)

    def check_scenario(self, key):
        self.check_type(key, dict)

    def check_triggers(self, key):
        self.check_type(key, list)

    def check_steps(self, key):
        self.check_type(key, list)

    def RaiseErrorMessage(self, IntersectionElement):
        common = ['common', 'action', 'notification']
        try:
            if IntersectionElement >= set(common):
                DiffElement = IntersectionElement - set(common)
                if len(DiffElement) == 0:
                    raise Exception("A key fields may be missing from: [scenario, triggers, steps]")
                if len(DiffElement) > 1:
                    raise Exception(f"{list(DiffElement)} can not exist at the  same time")
            else:
                missBasicKey = " or ".join([x for x in common if x not in IntersectionElement])
                raise Exception(f"Basic fields may be missing: {missBasicKey}")
        except Exception as e:
            raise e

class Check:

    def check_parameter(self, event):
        event_data = CheckParameters(event)
        input_keys = event_data.get_prefix_key()
        #---------------------------------检查字段缺失---------------------------------------------------------#
        _key_triggers = ['common', 'action', 'notification', 'triggers']
        _key_steps = ['common', 'action', 'notification',  'steps']
        _key_scenario = ['common', 'action', 'notification', 'scenario']
        _key_all = ['common', 'action', 'notification', 'scenario', 'triggers', 'steps']
        IntersectionElement = set(input_keys) & set(_key_all)      #--交集
        if any((IntersectionElement == set(_key_triggers), IntersectionElement == set(_key_steps), IntersectionElement == set(_key_scenario))):
            for key in input_keys:
                if key in _key_all:
                    #----检查内层每个字段------#
                    event_data.check_key(key)
        else:
            event_data.RaiseErrorMessage(IntersectionElement)
        return True


def lambda_handler(event, context):
    return Check().check_parameter(event)
    # 1. common 必须存在
    # 2. action 必须存在
    # 3. notification 必须存在
    # 4. scenario  triggers 和 steps 必须存在一个
