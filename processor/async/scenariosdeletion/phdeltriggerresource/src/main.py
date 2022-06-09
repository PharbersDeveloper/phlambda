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
        self.triggers = event["triggers"]

    def get_projectId(self):

        return self.event['projectId']

    def get_scenarioId(self):

        return self.event['scenario']['id']

    def get_stackName(self, triggerId):

        return get_stackName(get_stackName("-".join(["scenario", self.get_projectId(), self.get_scenarioId(), str(triggerId)])))


    def checkStackExisted(self, stackName):
        cf = boto3.client('cloudformation')
        try:
            stacks = cf.describe_stacks(StackName=stackName)['Stacks']
            if len(stacks) > 0:
                pass
        except Exception as e:
            print("*"*50 + "error" + "*"*50)
            print(str(e))
            raise Exception(f"{stackName}  not exist")

    def del_trigger_rule(self, stackName):
        print("*"*50 +"stackName" + "*"*50 + "\n" +stackName)
        processMessage = {}
        processMessage["Name"] = stackName
        #----- 检测stackName是否存在 -------------------#
        self.checkStackExisted(stackName)

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
            eachStackName = self.get_stackName(triggerId)
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

