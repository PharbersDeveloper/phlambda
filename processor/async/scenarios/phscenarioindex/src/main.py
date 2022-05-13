import json
import boto3
from boto3.dynamodb.conditions import Attr,Key

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

    def put_item(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scenario')
        response = table.put_item(
            Item={
                'projectId': self.get_projectId(),
                'id': self.get_id(),
                'active': self.get_active(),
                'args': self.get_args(),
                'index': self.get_index(),
                'owner': self.get_owner(),
                'projectName': self.get_projectName(),
                'scenarioName': self.get_scenarioName(),
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
        if Items[0]:
            OldImage = {
                "id": Items['id'],
                "active": Items['active'],
                "scenarioName": Items['scenarioName'],
                #"deletion": Items['deletion'],
                "index": Items['index']
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
    scenarioClient.get_OldImage()
    scenarioClient.put_item()

    return scenarioClient.fetch_result()


