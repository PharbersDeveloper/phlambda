import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
这个函数只做一件事情，将 trigger 的所有东西写到 scenario_trigger dynamodb中
args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": {
            "id": "scenario id",
            "active": true,
            "scenarioName": "scenario name",
            "deletion": false
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
                "id": "trigger id"
            }
        ]
    }
'''
class TriggersIndex:
    def __init__(self, event):
        self.event = event
        self.triggers = event['triggers']

    def get_traceId(self):
        return self.event['traceId']

    def get_projectId(self):
        return self.event['projectId']

    def put_item(self, scenarioId, TriggerId, active, detail, index, mode, traceId, name):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scenario_trigger')
        response = table.put_item(
            Item={
                'scenarioId': scenarioId,
                'id': TriggerId,
                'active': active,
                'detail': self.dumps_data_by_json(detail),
                'index': index,
                'mode': mode,
                'traceId': traceId,
                'name': name

            }
        )
        return response

    def query_table_item(self, tableName, partitionKey, sortKey, scenarioId, TriggerId):
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(scenarioId)
                                   & Key(sortKey).eq(TriggerId)
        )
        return res["Items"]

    def dumps_data_by_json(self, data):
        if isinstance(data, str):
            return data
        else:
            return json.dumps(data)

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data


    def get_OldImage(self, scenarioId, TriggerId):
        Items= self.query_table_item('scenario_trigger', 'scenarioId', 'id', scenarioId, TriggerId)
        print("*"*50+"trigger content " + "*"*50)
        print(Items)
        if len(Items) != 0:
            ItemDict = Items[0]
            OldImage = {
                "active": ItemDict['active'],
                "detail": ItemDict['detail'],
                "index": self.turn_decimal_into_int(ItemDict['index']),
                "mode": ItemDict['mode'],
                "id": ItemDict['id'],
                "scenarioId": ItemDict["scenarioId"],
                "name": ItemDict["name"]
            }
        else:
            OldImage = {}
        return OldImage


    def QueryAllItemsOfScenario(self, tableName, partitionKey, ValueOfpartitionKey):

        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(ValueOfpartitionKey)
        )

        return res["Items"]

    def GetNeedDeleteItems(self, scenarioId):

        AllScenarioItems = self.QueryAllItemsOfScenario("scenario_trigger", "scenarioId", scenarioId)
        AllScenarioKey = list(map(lambda x: {"id": x["id"], "scenarioId": x["scenarioId"]}, AllScenarioItems))
        CurrentTriggers= list(map(lambda x: {"id": x["id"], "scenarioId": x["scenarioId"]}, self.triggers))
        NeedDeleteKey = [x for x in AllScenarioKey if x not in CurrentTriggers]
        return NeedDeleteKey

    def get_trigger_stackName(self, triggerId):

        return str("-".join(["scenario", self.get_projectId(), str(triggerId)])).replace("_", "")

    def del_trigger_rule(self, stackName):
        print("*"*50 +"stackName" + "*"*50 + "\n" +stackName)
        processMessage = {}
        processMessage["Name"] = stackName

        try:
            client = boto3.client('cloudformation')
            response = client.delete_stack(
                StackName=stackName # event['runnerId']
            )
            processMessage['status'] = 'success'
            processMessage['message'] = f'delete {stackName} resource success'
            print(response)
        except Exception as e:
            print("*"*50 + "error" + "*"*50)
            print(str(e))
            processMessage['status'] = 'failed'
            processMessage['message'] = str(e)
        return processMessage

    def DeleteNotNeedItems(self):
        NeedDeleteKey = self.GetNeedDeleteItems(self.event["scenario"]["id"])
        #------ 删除 event rule ----------------#
        for item in NeedDeleteKey:
            #----- delete per event rule ---------------#
            self.del_trigger_rule(self.get_trigger_stackName(item['id']))
            #----- update item of trigger ---------------#
            self.del_table_item("scenario_trigger", "scenarioId", "id", item["scenarioId"], item["id"])

    def del_table_item(self, tableName, partitionKey, sortKey, partitionValue, sortValue):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        table.delete_item(
            Key={
                partitionKey: partitionValue,
                sortKey: sortValue
            },
        )

    def putTriggersItemIntoDyDB(self):
        #----更新items-----------------#
        self.DeleteNotNeedItems()

        for trigger in self.triggers:
            triggerId = trigger["id"]
            scenarioId = trigger["scenarioId"]
            detail = trigger["detail"]
            active = trigger["active"]
            index = trigger["index"]
            mode = trigger["mode"]
            name = trigger["name"]
            #-------- get oldImage -------------------------#
            oldImage = self.get_OldImage(scenarioId, triggerId)
            trigger["OldImage"] = oldImage
            #-------- put Trigger item int dyDB-----------------#
            self.put_item(scenarioId, triggerId, active, detail, index, mode, self.get_traceId(), name)
        return self.triggers

def lambda_handler(event, context):

    triggersClient = TriggersIndex(event)

    result = triggersClient.putTriggersItemIntoDyDB()

    return result