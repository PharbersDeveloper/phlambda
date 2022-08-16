import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal

'''
这个函数只做两件事情，
# 1. 将所有的错误都提取出来写入到notification中
2. 将创建成功但整体失败的东西会滚
'''

class RollBack:
    def __init__(self, event):
        self.event = event
        self.scenario = event['scenario']
        self.trigger = event['triggers']
        self.step = event['steps']
        self.reports = event['reports']
        self.errorMessage = {}
        print("*"*50+"event"+"*"*50)
        print(self.event)

    def get_projectId(self):
        return self.event['projectId']

    def get_scenarioId(self):
        return self.scenario['id']

    def get_traceId(self):
        return self.event['traceId']

    def get_owner(self):
        return self.event['owner']

    def get_projectName(self):
        return self.event['projectName']

    def check_OldImage(self, mode_type):
        try:
            if isinstance(mode_type, list) and len(mode_type) == 0:
                return "NotNeedRollBack"
            else:
                return "Delete" if len(mode_type['OldImage']) == 0 else "RollBack"
        except Exception as e:
            print("*"*50+"OldImage ERROR"+"*"*50 + "\n", str(e))
            return "NotNeedRollBack"

    def get_OldImage(self, mode_type):
        return mode_type['OldImage']

    def get_showName(self):
        return self.event['showName']

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
            'showName': self.get_showName(),
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
            'traceId': self.get_traceId()
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
            'traceId': self.get_traceId()
        }
        return step_Item

    def get_reportItem(self, OldImage):
        step_Item = {
            'scenarioId': OldImage["scenarioId"],
            'id': OldImage['id'],
            'detail': OldImage['detail'],
            'index': self.turn_decimal_into_int(OldImage['index']),
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
            "scenario_step": self.get_stepItem,
            "scenario_report": self.get_reportItem
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

        if len(self.scenario) == 0:
            self.NotNeedRollBack()
            pass
        else:
            RollBackMode = self.check_OldImage(self.scenario)
            print(f"Mode: {RollBackMode}")
            self.errorMessage['scenario'] = f"error handle mode: {RollBackMode}"
            if RollBackMode == "Delete":
                return self.map_handle_mode(RollBackMode)("scenario", "projectId", "id", self.get_projectId(), self.get_scenarioId())
            elif RollBackMode == "RollBack":
                return self.map_handle_mode(RollBackMode)(self.scenario, "scenario")
            else:
                return self.map_handle_mode(RollBackMode)()


    def triggerRollBack(self):
        countNum = 0
        for trigger in self.trigger:
            triggerId = trigger["id"]
            EachTriggerScenarioId = trigger["scenarioId"]
            RollBackMode = self.check_OldImage(trigger)
            print(f"Mode: {RollBackMode}")
            self.errorMessage['scenario_trigger_' + f"{countNum + 1}"] = f"error handle mode: {RollBackMode}"
            if RollBackMode == "Delete":
                return self.map_handle_mode(RollBackMode)("scenario_trigger", "scenarioId", "id", EachTriggerScenarioId, triggerId)
            elif RollBackMode == "RollBack":
                return self.map_handle_mode(RollBackMode)(trigger, "scenario_trigger")
            else:
                return self.map_handle_mode(RollBackMode)()

    def stepsRollBack(self):
        countNum = 0
        for step in self.step:
            stepId = step["id"]
            EachStepscenarioId = step["scenarioId"]
            RollBackMode = self.check_OldImage(self.step)
            print(f"Mode: {RollBackMode}")
            self.errorMessage['scenario_step_' + f"{str(countNum+1)}"] = f"error handle mode: {RollBackMode}"
            if RollBackMode == "Delete":
                return self.map_handle_mode(RollBackMode)("scenario_step", "scenarioId", "id", EachStepscenarioId, stepId)
            elif RollBackMode == "RollBack":
                return self.map_handle_mode(RollBackMode)(step, "scenario_step")
            else:
                return self.map_handle_mode(RollBackMode)()

    def ReportsRollBack(self):
        countNum = 0
        for report in self.reports:
            reportId = report["id"]
            EachReportScenarioId = report["scenarioId"]
            RollBackMode = self.check_OldImage(self.reports)
            print(f"Mode: {RollBackMode}")
            self.errorMessage['scenario_report_' + f"{str(countNum+1)}"] = f"error handle mode: {RollBackMode}"
            if RollBackMode == "Delete":
                return self.map_handle_mode(RollBackMode)("scenario_report", "scenarioId", "id", EachReportScenarioId, reportId)
            elif RollBackMode == "RollBack":
                return self.map_handle_mode(RollBackMode)(report, "scenario_report")
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
        return {"type": "notification", "opname": self.get_owner(),
                "cnotification": {"data": {"datasets": []}, "error": self.errorMessage}}

def lambda_handler(event, context):

    try:
        #-------------------回滚操作-----------------------------------#
        rollBackClient = RollBack(event)
        rollBackClient.scenarioRollBack()
        rollBackClient.triggerRollBack()
        rollBackClient.stepsRollBack()
        rollBackClient.ReportsRollBack()

        return rollBackClient.fetch_result()
    except Exception as e:
        print(f'UNKnonw ERROR: {str(e)}')
        return {"type": "notification", "opname": event['owner'],
                "cnotification": {"data": {"datasets": []}, "error": str(e)}}
