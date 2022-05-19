import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime

'''
删除cloudformation 里面的东西 rule

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scenario.$": "$.scenario",
        "triggers.$": "$.triggers"
    }
'''

class DelTriggerRule:

    def __int__(self, event):
        self.event = event
        self.result = {}

    def get_projectId(self):

        return self.event['projectId']

    def get_scenarioId(self):

        return self.event['scenario']

    def get_triggerId(self):

        return self.event['triggers']

    def get_stackName(self):

        return "-".join(["scenario", self.get_projectId(), self.get_scenarioId(), self.get_triggerId()])

    def del_trigger_rule(self, stackName):
        try:
            client = boto3.client('cloudformation')
            response = client.delete_stack(
                StackName=stackName # event['runnerId']
            )
            self.result['status'] = 'ok'
            self.result['message'] = f'delete {stackName} resource success'
        except Exception as e:
            self.result['status'] = 'error'
            self.result['message'] = str(e)


def lambda_handler(event, context):

    delRuleClient = DelTriggerRule(event)
    delRuleClient.del_trigger_rule(delRuleClient.get_stackName())

    return delRuleClient.result
