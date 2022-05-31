import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
在executionV2执行结束后获取执行的状态 
成功index+1
    如果index+1 == count scenario结束 status==succeed
    如果index+1 != count scenario继续 status==running
失败查看ignore-error参数
    如果为false scenario 结束 status == failed
    如果为true scenario继续 index+1 
        如果 index+1 == count scenario结束 status==succeed
        如果index+1 != count scenario继续 status==running
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
    scenarioClient.get_OldImage()
    scenarioClient.put_item()

    return scenarioClient.fetch_result()


