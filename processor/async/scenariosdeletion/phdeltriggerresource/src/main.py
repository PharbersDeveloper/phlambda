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


def reduce_length_of_stackName(stackName):
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
        return reduce_length_of_stackName(stackName)


class DelTriggerRule(object):

    def __init__(self, event):
        self.event = event
        self.triggers = event["triggers"]

    def get_projectId(self):

        return self.event['projectId']

    def get_stackName(self, scenarioId, triggerId):

        return reduce_length_of_stackName("-".join(["scenario", self.get_projectId(), str(scenarioId), str(triggerId)]))

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

    def DeleteEachTriggerResource(self):

        triggerCountNum = 0
        DeleteTriggersResultList = []

        for trigger in self.triggers:
            triggerId = trigger["id"]
            scenarioId = trigger["scenarioId"]
            eachStackName = self.get_stackName(scenarioId, triggerId)
            #------------ delete trigger resource ---------#
            EachDeleteResult = self.del_trigger_rule(eachStackName)
            EachDeleteResult["index"] = triggerCountNum + 1
            DeleteTriggersResultList.append(EachDeleteResult)

        return DeleteTriggersResultList


def lambda_handler(event, context):

    delRuleClient = DelTriggerRule(event)

    #------- 返回结果是数组，包含每一个trigger的删除结果 -----------#
    result = delRuleClient.DeleteEachTriggerResource()

    return {"type": "notification", "opname": event['owner'],
                        "cnotification": {"data": {"datasets": "", "error": result}}}

