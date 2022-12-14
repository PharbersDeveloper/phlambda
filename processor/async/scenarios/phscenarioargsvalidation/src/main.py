import json
import boto3
from boto3.dynamodb.conditions import Attr, Key

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
            "id": "scenario id",       # 如果有就是update，如果没有就是新建
            "active": true,
            "scenarioName": "scenario name",
            # "deletion": true | false      # 如果是true，则所有和scenario相关的全部删除
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
        #------ 参数类型 -------#
        self.check_dict = {
            "common": dict,
            "action": dict,
            "notification": dict,
            "scenario": dict,
            "triggers": list,
            "steps": list,
            "reports": list
        }


    def get_prefix_key(self):

        return list(self.event.keys())

    def check_key(self, key):

        InputParameterType = self.check_dict[key]

        return self.Check_Parameter_Type(key, InputParameterType)

    def Check_Parameter_Type(self, key, InputParameterType):
        try:
            if isinstance(self.event[key], InputParameterType) is False:
                raise Exception(f"type error: {key} is not belong {str(InputParameterType)}")
        except Exception as e:
            raise e


class Check:

    def query_scenario(self, projectId, scenarioName):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("scenario")
        response = table.query(
            IndexName='projectId-scenarioName-index',
            KeyConditionExpression=Key('projectId').eq(projectId) & Key('scenarioName').eq(scenarioName)
        )
        return response.get("Items")


    def check_parameter(self, event):
        event_data = CheckParameters(event)
        input_keys = event_data.get_prefix_key()
        #---------------------------------检查字段缺失---------------------------------------------------------#
        _key_triggers = ['common', 'action', 'notification', 'scenario', 'triggers']
        _key_steps = ['common', 'action', 'notification', 'scenario',  'steps']
        _key_reports = ['common', 'action', 'notification', 'scenario',  'reports']
        _key_all = ['common', 'action', 'notification', 'scenario', 'triggers', 'steps', 'reports']
        if any((set(input_keys) >= set(_key_triggers), set(input_keys) >= set(_key_steps),
                set(input_keys) >= set(_key_reports), set(input_keys) >= set(_key_all))):
            for key in input_keys:
                if key in _key_all:
                    #----检查内层每个字段------#
                    event_data.check_key(key)
        else:
            missing_field = " or ".join([x for x in _key_all if x not in input_keys])
            raise Exception(f"Field missing: {input_keys} possible missing fields {missing_field}")

        #----- 张玉磊 ScenarioName 重复验证 ------#
        for scenario in self.query_scenario(event.get("common").get("projectId"),
                                            event.get("scenario").get("scenarioName")):
            if scenario["id"] != event.get("scenario").get("id"):
                raise Exception(f"scenario name already exist")

        return True

def lambda_handler(event, context):

    return Check().check_parameter(event)

# 1. common 必须存在
# 2. action 必须存在
# 3. notification 必须存在
# 4. scenario 必须存在
# 5. triggers 和 steps 必须存在一个