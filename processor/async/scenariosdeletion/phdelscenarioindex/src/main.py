import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from datetime import datetime

'''
删除 scenario 里面的东西

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": "$.scenario"
    }
'''

class DelScenarioIndex:

    def __init__(self, event):
        self.event = event

    def get_projectId(self):
        return self.event['projectId']

    def get_scenarioId(self):
        return self.event['id']

    def del_table_item(self, tableName, **kwargs):

        DelItem = dict(kwargs.items())
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        table.delete_item(
            Key=DelItem,
        )

    #TODO 因为scenario为父级，所以需同时获取子级的OldImage,现在不知道返回的数据结果，后面对接的时候再做
    def get_OldImage(self):
        pass

    def fetch_result(self):
        return True


def lambda_handler(event, context):
    DelClient = DelScenarioIndex(event)
    #-------------------delete step---------------------------------------------#
    #TODO 删除Item前需将数据保存到OldImage，以便后面回滚操作时用
    DelClient.del_table_item('scenario_step', scenarioId=DelClient.get_scenarioId())
    #-------------------delete trigger---------------------------------------------#
    DelClient.del_table_item('scenario_trigger', scenarioId=DelClient.get_scenarioId())
    #-------------------delete scenario---------------------------------------------#
    DelClient.del_table_item('scenario', projectId=DelClient.get_projectId(), id=DelClient.get_scenarioId())
    return DelClient.fetch_result()


