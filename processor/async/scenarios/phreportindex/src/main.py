import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

'''
这个函数只做一件事情，将 scenario reports 的所有东西写到 scenario_report dynamodb中
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
        "reports": [
            {
                "detail": {
                    "type":"EMAIL",
                    "destination":"test@qq.com"
                },
                "index": 0,
                "mode": "dataset",
                "name": "alfred",
                "id": "step id",
            }
        ]
    }

return = {
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
            "mode": "dataset",
            "name": "alfred",
            "id": "step id",
            "oldImage": {
                "confData": {},
                "detail": {
                    "type":"dataset",
                    "recursive":false,
                    "ignore-error":false,
                    "name":"1235"
                },
                "index": 0,
                "mode": "dataset",
                "name": "alfred",
                "id": "step id",
            }
        }
    ]
}
'''

class ReportIndex:
    def __init__(self, event):
        self.event = event
        self.reports = event['reports']

    def get_traceId(self):
        return self.event['traceId']

    def dumps_data_by_json(self, data):
        if isinstance(data, str):
            return data
        else:
            return json.dumps(data)

    def put_item(self, scenarioId, reportID,  detail, index, mode, name, traceId):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('scenario_report')
        response = table.put_item(
            Item={
                'scenarioId': scenarioId,
                'id': reportID,
                'detail': self.dumps_data_by_json(detail),
                'index': index,
                'mode': mode,
                'name': name,
                'traceId': traceId
            }
        )
        return response

    def query_table_item(self, tableName, partitionKey, sortKey, scenarioId, reportId):
        dynamodb = boto3.resource('dynamodb')
        ds_table = dynamodb.Table(tableName)
        res = ds_table.query(
            KeyConditionExpression=Key(partitionKey).eq(scenarioId)
                                   & Key(sortKey).eq(reportId)
        )
        return res["Items"]

    def turn_decimal_into_int(self, data):
        return int(data) if isinstance(data, Decimal) else data

    def get_OldImage(self, scenarioId, reportId):
        Items= self.query_table_item('scenario_report', 'scenarioId', 'id', scenarioId, reportId)
        print("*"*50+"report content"+"*"*50)
        print(Items)
        if len(Items) != 0:
            ItemDict = Items[0]
            OldImage = {
                "detail": ItemDict['detail'],
                "index": self.turn_decimal_into_int(ItemDict['index']),
                "mode": ItemDict['mode'],
                "name": ItemDict['name'],
                "id": ItemDict['id'],
                "scenarioId": ItemDict["scenarioId"],
                "traceId": ItemDict["traceId"]
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

        AllScenarioItems = self.QueryAllItemsOfScenario("scenario_step", "scenarioId", scenarioId)
        AllScenarioKey = list(map(lambda x: {"id": x["id"], "scenarioId": x["scenarioId"]}, AllScenarioItems))
        CurrentReports = list(map(lambda x: {"id": x["id"], "scenarioId": x["scenarioId"]}, self.reports))
        NeedDeleteKey = [x for x in AllScenarioKey if x not in CurrentReports]
        return NeedDeleteKey

    def DeleteNotNeedItems(self):
        NeedDeleteKey = self.GetNeedDeleteItems(self.event["scenario"]["id"])
        for item in NeedDeleteKey:
            self.del_table_item("scenario_report", "scenarioId", "id", item["scenarioId"], item["id"])

    def del_table_item(self, tableName, partitionKey, sortKey, partitionValue, sortValue):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        table.delete_item(
            Key={
                partitionKey: partitionValue,
                sortKey: sortValue
            },
        )


    def putStepItemIntoDyDB(self):
        #-------更新当前item--------------------#
        self.DeleteNotNeedItems()

        for report in self.reports:
            reportID = report["id"]
            scenarioId = report["scenarioId"]
            detail = report["detail"]
            index = report["index"]
            mode = report["mode"]
            name = report["name"]
            #-------- get oldImage -------------------------#
            oldImage = self.get_OldImage(scenarioId, reportID)
            report["OldImage"] = oldImage
            #-------- put report item int dyDB-----------------#
            self.put_item(scenarioId, reportID,  detail, index, mode, name, self.get_traceId())
        return self.reports


def lambda_handler(event, context):

    StepsClient = ReportIndex(event)

    result = StepsClient.putStepItemIntoDyDB()

    return result