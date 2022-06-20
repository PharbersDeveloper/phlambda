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
        self.common = event['common']
        self.scenario = event['scenario']
        self.triggers = event['triggers']
        self.steps = event['steps']
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
            print("*" * 50 + "error" + "*" * 50 + "\n", str(e))
            raise e


    def check_common(self, key):
        self.check_type(key, dict)
        common_data = self.event["common"]
        common_list = ["traceId", "projectId", "projectName", "owner", "showName"]
        for elem in list(common_data.keys()):
            if elem not in common_list or str(common_data[elem]) == 0:
                raise Exception(f"{elem} not exist or  empty.")

    def check_action(self, key):
        self.check_type(key, dict)

    def check_notificaton(self, key):
        self.check_type(key, dict)

    def check_scenario(self, key):
        self.check_type(key, list)
        if len(self.scenario) == 0:
            pass
        else:
            for scenario in self.scenario:
                scenarioId = scenario["id"]
                self.check_DsData_Exists('scenario', **{"projectId": self.get_projectId(), "id": scenarioId})

    def check_triggers(self, key):
        self.check_type(key, list)
        for trigger in self.triggers:
            triggerId = trigger["id"]
            scenarioId = trigger["scenarioId"]
            self.check_DsData_Exists('scenario_trigger', **{"scenarioId": scenarioId, "id": triggerId})
            #--------- 检测stackName --------------------#
            stackName = self.get_stackName(triggerId)
            self.checkStackExisted(stackName)

    def check_steps(self, key):
        self.check_type(key, list)
        for step in self.steps:
            stepId = step["id"]
            scenarioId = step["scenarioId"]
            self.check_DsData_Exists('scenario_step', **{"scenarioId": scenarioId, "id": stepId})

    def get_stackName(self, triggerId):

        return str("-".join(["scenario", self.get_projectId(), str(triggerId)])).replace("_", "")


    def checkStackExisted(self, stackName):
        cf = boto3.client('cloudformation')
        try:
            stacks = cf.describe_stacks(StackName=stackName)['Stacks']
            if len(stacks) > 0:
                pass
        except Exception as e:
            print("*"*50 + "error" + "*"*50)
            print(str(e))
            raise Exception(f"{stackName}  not exist")

    def get_projectId(self):
        return self.common['projectId']


    #-------检查表中数据是否存在----------------------#
    def check_DsData_Exists(self, tableName, **kwargs):
        queryConditionDict = dict(kwargs.items())
        Item = self.query_table_item(tableName, **queryConditionDict)
        if len(Item) == 0:
            raise Exception(f"{queryConditionDict} not exists, please check you data.")

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


    def RaiseErrorMessage(self, IntersectionElement):
        common = ['common', 'action', 'notification']
        try:
            if IntersectionElement >= set(common):
                DiffElement = IntersectionElement - set(common)
                if len(DiffElement) == 0:
                    raise Exception("A key fields may be missing from: [scenario, triggers, steps]")
                #-------- 字段同时存在检测 --------------------------------#
                if any(["scenario" and "triggers" in DiffElement, "steps" in DiffElement]) is False:
                    raise Exception(f"scenario,triggers or steps may be missing in {list(DiffElement)}")
            #if len(DiffElement) > 1:
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
        _key_scenario = ['common', 'action', 'notification', 'scenario']
        _key_triggers = ['common', 'action', 'notification', 'triggers']
        _key_steps = ['common', 'action', 'notification', 'steps']
        _key_all = ['common', 'action', 'notification', 'scenario', 'triggers', 'steps']
        IntersectionElement = set(input_keys) & set(_key_all)      #--交集
        print((IntersectionElement))
        print(IntersectionElement == set(_key_steps))
        if any((IntersectionElement == set(_key_scenario), IntersectionElement == set(_key_steps), IntersectionElement == set(_key_triggers), IntersectionElement == set(_key_all))):
            for key in input_keys:
                if key in _key_all:
                    #----检查内层每个字段------#
                    print(key)
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
