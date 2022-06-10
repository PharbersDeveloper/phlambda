import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
这个函数只做一件事情，将scenario的所有东西写到Scenario dynamodb中
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
            "deletion": false, --舍弃
            "index": "index"
        }
    }
'''
class ScenarioIndex:
    def __init__(self, event):
        self.event = event
        self.scenario = self.event['scenario']

    def get_projectId(self):
        return self.event['projectId']

    def get_id(self):
        return self.scenario['id']

    def get_active(self):
        return self.scenario['active']

    def get_args(self):
        return ''

    def get_index(self):
        return self.scenario['index']

    def get_owner(self):
        return self.event['owner']

    def get_projectName(self):
        return self.event['projectName']

    def get_scenarioName(self):
        return self.scenario['scenarioName']

    def get_traceId(self):
        return self.event['traceId']

    def get_showName(self):
        return self.event['showName']

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data

    def put_item(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scenario')
        response = table.put_item(
            Item={
                'projectId': self.get_projectId(),
                'id': self.get_id(),
                'active': self.get_active(),
                'args': self.get_args(),
                'index': self.turn_decimal_into_int(self.get_index()),
                'owner': self.get_owner(),
                'projectName': self.get_projectName(),
                'scenarioName': self.get_scenarioName(),
                'showName': self.get_showName(),
                'traceId': self.get_traceId()
                }
        )
        return response

    def query_table_item(self, tableName, partitionKey, sortKey):
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(self.get_projectId())
                                   & Key(sortKey).eq(self.get_id())
        )
        return res["Items"]

    def get_OldImage(self):
        Items= self.query_table_item('scenario', 'projectId', 'id')
        print("*"*50+"OldImage contents"+"*"*50)
        print(Items)
        if len(Items) != 0:
            ItemDict = Items[0]
            OldImage = {
                "id": ItemDict['id'],
                "active": ItemDict['active'],
                "scenarioName": ItemDict['scenarioName'],
                "index": self.turn_decimal_into_int(ItemDict['index'])
            }
        else:
            OldImage = {}
        self.OldImage = OldImage
        return OldImage

    def fetch_result(self):
        self.scenario['OldImage'] = self.OldImage
        return self.scenario

def lambda_handler(event, context):

    scenarioClient = ScenarioIndex(event)
    #------ scenario 输入为空的情况 --------#
    if len(scenarioClient.scenario) == 0:
        return scenarioClient.scenario
    else:
        scenarioClient.get_OldImage()
        scenarioClient.put_item()
        return scenarioClient.fetch_result()


