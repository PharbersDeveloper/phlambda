import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal


class FetchTriggersAndStepsFromScenarioId:

    def __init__(self, event):
        self.event = event
        self.scenario = event['scenario']

    def query_table_item(self, tableName, partitionKey, ValueOfpartitionKey):

        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(ValueOfpartitionKey)
        )

        return res["Items"]

    def ChangeStringToDict(self, StringData):

        return StringData if isinstance(StringData, dict) else json.loads(StringData)

    def ChangeDecimalToInt(self, data):

        return int(data) if isinstance(data, Decimal) else data

    def MakeEachTriggerItem(self, EachTriggerItem):
        TriggerItem = {
            "active": EachTriggerItem['active'],
            "detail": self.ChangeStringToDict(EachTriggerItem['detail']),
            "index": self.ChangeDecimalToInt(EachTriggerItem['index']),
            "mode": EachTriggerItem['mode'],
            "id": EachTriggerItem['id'],
            "scenarioId": EachTriggerItem['scenarioId']
        }
        return TriggerItem

    def MakeEachStepItem(self, EachStepItem):
        StepItem = {
            "confData": EachStepItem["confData"],
            "detail": self.ChangeStringToDict(EachStepItem["detail"]),
            "index": self.ChangeDecimalToInt(EachStepItem["index"]),
            "mode": EachStepItem["mode"],
            "name": EachStepItem["name"],
            "id": EachStepItem["id"],
            "scenarioId": EachStepItem['scenarioId']
        }
        return StepItem

    def GetTriggersItemsFromScenarioId(self):

        ItemsOfQuery = self.query_table_item("scenario_trigger", "scenarioId", self.scenario["id"])
        AllTriggersItems = []
        for Item in ItemsOfQuery:
            EachTrigggerItem = self.MakeEachTriggerItem(Item)
            AllTriggersItems.append(EachTrigggerItem)
        return AllTriggersItems


    def GetStepsItemsFromScenarioId(self):
        ItemsOfQuery = self.query_table_item("scenario_step", "scenarioId", self.scenario["id"])
        AllStepsItems = []
        for Item in ItemsOfQuery:
            EachStepItem = self.MakeEachStepItem(Item)
            AllStepsItems.append(EachStepItem)
        return AllStepsItems


    def FetchItemsFromScenarioId(self):

        if len(self.scenario) == 0:
            triggersItems = self.event["triggers"]
            stepsItems = self.event["steps"]
        else:
            triggersItems = self.GetTriggersItemsFromScenarioId()
            stepsItems = self.GetStepsItemsFromScenarioId()

        return {
            "triggers": triggersItems,
            "steps": stepsItems
        }

def lambda_handler(event, context):

    FetchClient = FetchTriggersAndStepsFromScenarioId(event)

    TriggersAndStepItems = FetchClient.FetchItemsFromScenarioId()

    print(TriggersAndStepItems)

    return TriggersAndStepItems
