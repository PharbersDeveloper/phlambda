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


class DelTriggerRule(object):

    def __init__(self, event):
        self.event = event
        self.triggers = event["triggers"]

    def get_projectId(self):

        return self.event['projectId']

    def get_stackName(self, triggerId):
        '''
        "_" 不满足stackName拼写规则
        example:
        1 validation error detected: Value 'scenario-ggjpDje0HUC2JW-cb6cb0afbf85c6e6_JCHeDjg-EB77EE5E' at 'stackName' failed to satisfy constraint: Member must satisfy regular expression pattern: [a-zA-Z][-a-zA-Z0-9]*|arn:[-a-zA-Z0-9:/._+]*
        An error occurred (ValidationError) when calling the DescribeStacks operation: 1 validation error detected: Value 'scenario-ggjpDje0HUC2JW-cb6cb0afbf85c6e6_JCHeDjg-EB77EE5E' at 'stackName' failed to satisfy constraint: Member must satisfy regular expression pattern: [a-zA-Z][-a-zA-Z0-9]*|arn:[-a-zA-Z0-9:/._+]*
        '''

        return str("-".join(["scenario", self.get_projectId(), str(triggerId)])).replace("_", "")

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
            #scenarioId = trigger["scenarioId"]
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

