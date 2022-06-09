import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from reduceLengthOfstackName import reduce_length_of_stackName
from decimal import Decimal

'''
这个函数只做一件事情，检查参数是否合法
{
  "common": {
    "traceId": "alfred-resource-creation-traceIdw22234",
    "tenantId": "pharbers",
    "projectId": "HU3n443YN3IO6Rt",
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
    "id": "HU3n443YN3IO6Rt_601c6865249e475682064652d0745881wwwww",
    "active": true,
    "scenarioName": "scenario name",
    "deletion": false
  },
  "triggers": [
    {
      "active": true,
      "detail": {
        "timezone": "中国北京",
        "start": "2022-04-26 16:10:14",
        "period": "minute",
        "value": 1
      },
      "index": 0,
      "mode": "timer",
      "id": "093B40B9BC51CB76"
    }
  ],
  "steps": [
    {
      "confData": {},
      "detail": {
        "type": "dataset",
        "recursive": false,
        "ignore-error": false,
        "name": "1235"
      },
      "index": 0,
      "mode": "dataset",
      "name": "alfred",
      "id": "step id"
    }
  ],
  "result": {}
}
'''



class FetchTriggersAndStepsFromScenarioId:

    def __init__(self, event):
        self.event = event
        self.scenario = event['scenario']


    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data


    def query_table_item(self, tableName, partitionKey, ValueOfpartitionKey):

        #dynamodb = boto3.resource('dynamodb')
        dynamodb = boto3.resource('dynamodb', region_name='cn-northwest-1', aws_access_key_id='AKIAWPBDTVEANKEW2XNC',
                            aws_secret_access_key='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')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression= Key(partitionKey).eq(ValueOfpartitionKey)
        )

        return res["Items"]

    def dumps_data_by_json(self, data):
        if isinstance(data, str):
            return data
        else:
            return json.dumps(data)

    def GetTriggersItemsFromScenarioId(self):

        ItemsOfQuery = self.query_table_item("scenario_trigger", "scenarioId", self.scenario["id"])
        for Item in ItemsOfQuery:

            print(Item)



    def GetStepsItemsFromScenarioId(self):
        pass

    def FetchItemsFromScenarioId(self):

        if len(self.scenario) == 0:
            triggersItems = self.event["triggers"]
            stepsItems = self.event["steps"]
        else:
            triggersItems = self.GetTriggersItemsFromScenarioId()
            stepsItems = self.GetStepsItemsFromScenarioId()

        return triggersItems, stepsItems

def lambda_handler(event, context):

    FetchClient = FetchTriggersAndStepsFromScenarioId(event)
    FetchClient.GetTriggersItemsFromScenarioId()

    #fetchData = FetchClient.FetchItemsFromScenarioId()

    return ""

if __name__ == '__main__':
    event = {
        "common": {
            "traceId": "alfred-resource-creation-traceIdw22234",
            "tenantId": "pharbers",
            "projectId": "HU3n443YN3IO6Rt",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred"
        },
        "action": {
            "cat": "createOrUpdateScenario",
            "desc": "create or update scenario",
            "comments": "something need to say",
            "message": "something need to say",
            "required": True
        },
        "notification": {
            "required": True
        },
        "scenario": {
            "id": "ggjpDje0HUC2JW_55a080cb402943869f3a1519bef2b989",
            "active": True,
            "scenarioName": "scenario name",
            "deletion": False
        },
        "triggers": [
            {
                "active": True,
                "detail": {
                    "timezone": "中国北京",
                    "start": "2022-04-26 16:10:14",
                    "period": "minute",
                    "value": 1
                },
                "index": 0,
                "mode": "timer",
                "id": "093B40B9BC51CB76"
            }
        ],
        "steps": [
            {
                "confData": {},
                "detail": {
                    "type": "dataset",
                    "recursive": False,
                    "ignore-error": False,
                    "name": "1235"
                },
                "index": 0,
                "mode": "dataset",
                "name": "alfred",
                "id": "step id"
            }
        ],
        "result": {}
    }

    lambda_handler(event, "")
