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

def get_stackName(stackName):
    import re
    #----------限制字符串长度---------------------#
    if len(stackName) <= 62:
        return stackName
    else:
        data = str(stackName).split('-')
        scenario = data[0]
        projectId = data[1]
        #--------取奇数,反转，切片---------------#
        scenarioId = ''.join(reversed(str(data[2])[::2]))
        #--------取偶数-----------------#
        triggerId = str(data[3])[1::2]
        if len(data) > 4:
            timeTag = re.sub(pattern='[-:\s+.]', repl='', string=''.join(data[4:]))
            stackName = '-'.join([scenario, projectId, scenarioId, triggerId, timeTag])
        else:
            stackName = '-'.join([scenario, projectId, scenarioId, triggerId])
        return get_stackName(stackName)


class DelTriggerRule(object):

    def __init__(self, event):
        self.event = event
        self.result = {}

    def get_projectId(self):

        return self.event['projectId']

    def get_scenarioId(self):

        return self.event['scenario']['id']

    def get_triggerId(self):

        return self.event['triggers'][0]['id']

    def get_stackName(self):

        return get_stackName(get_stackName("-".join(["scenario", self.get_projectId(), self.get_scenarioId(), self.get_triggerId()])))

    def del_trigger_rule(self, stackName):
        print("*"*50 +"stackName" + "*"*50 + "\n" +stackName)
        try:
            client = boto3.client('cloudformation')
            response = client.delete_stack(
                StackName=stackName # event['runnerId']
            )
            self.result['status'] = 'ok'
            self.result['message'] = f'delete {stackName} resource success'
            print(response)
        except Exception as e:
            print("*"*50 + "error" + "*"*50)
            print(str(e))
            self.result['status'] = 'error'
            self.result['message'] = str(e)

def lambda_handler(event, context):

    delRuleClient = DelTriggerRule(event)

    delRuleClient.del_trigger_rule(delRuleClient.get_stackName())

    return delRuleClient.result
