import json
import boto3
import traceback
import time
from datetime import datetime
from exceptions import ScenarioResourceError, ScenarioStackNotExistError
from gencronexpression import GenCronExpression
import os

'''
这个函数只做一件事情，通过比较更新的内容，查看是否需要创建cf 来更新 timer资源
args:
    event = {
        "tenantId.$":"$.common.tenantId",
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
        "triggers": [
            {
                "active": true,
                "detail": {
                    "timezone":"中国北京",
                    "start":"2022-04-26 16:10:14",
                    "period":"minute",
                    "value":1
                    "cron":""
                },
                "index": 0,
                "mode": "timer",
                "id": "trigger id"
                "oldimage": {
                    "active": true,
                    "detail": {
                        "timezone":"中国北京",
                        "start":"2022-04-26 16:10:14",
                        "period":"minute",
                        "value":1
                    },
                    "index": 0,
                    "mode": "timer",
                    "id": "trigger id"
                }
            }
        ]
    }
'''
class TriggersResources:
    def __init__(self, tenantId, targetArn, projectId, scenarioId, triggerId, cronExpression, templateUrl):
        self.cf = boto3.client('cloudformation')
        self.current_time = (datetime.now()).strftime('%Y-%m-%d-%H-%M-%S')
        self.stackName = self.GetStackName()
        self.tenantId, self.targetArn, self.projectId, self.scenarioId, self.triggerId, self.cronExpression = \
            tenantId, targetArn, projectId, scenarioId, triggerId, cronExpression
        self.result = {}
        self.template_url = templateUrl

    def get_checkDict(self):
        checkDict = {
            "BusName": "default",
            "ScheduleExpression": self.cronExpression,
            "TenantId": self.tenantId,
            "ScenarioId": self.scenarioId,
            "TriggerId": self.triggerId,
            "ProjectId": self.projectId,
            "TargetArn": self.targetArn,
            "TimerName": self.stackName
        }
        return checkDict

    def getStackExisted(self):
        try:
            stacks = self.cf.describe_stacks(StackName=self.stackName)['Stacks']
            if len(stacks) > 0:
                return stacks[0]
        except Exception:
            raise ScenarioStackNotExistError('stack not exist error')

    def checkStackStatus(self):
        print('check status ============>')
        stack = self.getStackExisted()
        print(stack['StackStatus'])
        if stack['StackStatus'] != "UPDATE_COMPLETE" and stack['StackStatus'] != "CREATE_COMPLETE":
            raise ScenarioResourceError('stack is updating or createing, please update later')
        return stack

    def checkNeedUpdateResouce(self, stack):
        params = stack['Parameters']
        checkDict = self.get_checkDict()
        result = False
        for item in params:
            result |= item['ParameterValue'] != checkDict[item['ParameterKey']]
        return result

    def not_need_update(self):
        self.result['status'] = 'ok'
        self.result['message'] = f'resource {self.stackName} does not need to be updated'

    def ScenarioResourceError(self, error_message):
        self.result['status'] = 'error'
        self.result['message'] = f"{self.stackName} create failed and error: " + str(error_message)

    def get_Parameters(self):
        Parameters = [
            {
                "ParameterKey": "TimerName",
                "ParameterValue": self.stackName
            },
            {
                "ParameterKey": "ScheduleExpression",
                "ParameterValue": self.cronExpression
            },
            {
                "ParameterKey": "TenantId",
                "ParameterValue": self.tenantId
            },
            {
                "ParameterKey": "ScenarioId",
                "ParameterValue": self.scenarioId
            },
            {
                "ParameterKey": "TriggerId",
                "ParameterValue": self.triggerId
            },
            {
                "ParameterKey": "ProjectId",
                "ParameterValue": self.projectId
            },
            {
                "ParameterKey": "TargetArn",
                "ParameterValue": self.targetArn
            },
        ]
        return Parameters

    def GetStackName(self):
        return str("-".join(["scenario", self.projectId, self.triggerId])).replace("_", "")

    def GetChangeSetName(self, StackName, NowTime):
        return str("-".join([StackName, NowTime])).replace("_", "")

    def update_trigger(self):
        print("*"*50 + "  Update  " + "*"*50)
        changeSetName = self.GetChangeSetName(self.stackName, self.current_time)
        response = self.cf.create_change_set(
            StackName=self.stackName,
            ChangeSetName=changeSetName,
            TemplateURL=self.template_url,
            Parameters=self.get_Parameters()
        )

        while True:
            time.sleep(2)
            response = self.cf.describe_change_set(
                ChangeSetName=changeSetName,
                StackName=self.stackName
            )
            if response['Status'] == 'CREATE_COMPLETE':
                break
        self.cf.execute_change_set(
            ChangeSetName=changeSetName,
            StackName=self.stackName
        )
        self.result['status'] = 'ok'
        self.result['message'] = f'updating resource {self.stackName}'

    def create_trigger(self):
        print("*"*50 + " Create  " + "*"*50)
        response = self.cf.create_stack(
            StackName=self.stackName,
            TemplateURL=self.template_url,
            Parameters=self.get_Parameters()
        )
        print("*"*50 + " 创建完毕, create trigger Reponse " + "*"*50 + "\n", response)

        self.result['status'] = 'ok'
        self.result['message'] = f'create resource {self.stackName} '


def lambda_handler(event, context):
    print("*"*50 + " event " + "*"*50)
    print(event)

    tenantId = event['tenantId']
    targetArn = os.getenv("TARGETARN")
    projectId = event['projectId']

    if len(event['triggers']) == 0:
        result = {}
        result['status'] = 'error'
        result['message'] = 'triggers is not exists, can not create any resources.'
        #return result
        return {"type": "notification", "opname": event['owner'],
                       "cnotification": {"data": {"datasets": "", "error": result}}}
    else:
        #---------- 处理每一个trigger ------------------------------#
        messageList = []
        for trigger in event["triggers"]:
            triggerId = trigger['id']
            EachScenarioId = trigger["scenarioId"]
            #------- 拼cron表达式------------------------------------#
            start_time = trigger['detail']['start']
            period = trigger['detail']['period']
            value = trigger['detail']['value']
            cronExpression = GenCronExpression(start_time, period, value).get_cron_expression()
            print(cronExpression)
            templateUrl = os.getenv("TEMPLATEURL")

            triggers = TriggersResources(tenantId, targetArn, projectId, EachScenarioId, triggerId, cronExpression, templateUrl)

            try:
                stack = triggers.checkStackStatus()
                print("*"* 50 + "STack" + "*"*50 + "\n", stack)
                #--------------更新逻辑------------------------------#
                if triggers.checkNeedUpdateResouce(stack):
                    try:
                        triggers.update_trigger()
                    except Exception as e:
                        print("*"*50 + "打印更新错误日志" + "*"*50)
                        print(str(e))
                        triggers.result['status'] = 'error'
                        triggers.result['message'] = str(e)
                else:
                    triggers.not_need_update()
            except ScenarioStackNotExistError:
                #--------------创建逻辑-------------------------------#
                try:
                    triggers.create_trigger()
                except Exception as e:
                    print("*"*50 + "打印创建错误日志" + "*"*50)
                    print(str(e))
                    triggers.result['status'] = 'error'
                    triggers.result['message'] = str(e)
            except ScenarioResourceError as e:
                traceback_output = traceback.format_exc()
                print(traceback_output)
                triggers.ScenarioResourceError(e)
            except Exception:
                print('unknown error ===========>')
                traceback_output = traceback.format_exc()
                print(traceback_output)
            finally:
                print("--"*50 + "RESULT" + "--"*50)
                print(triggers.result)
                messageList.append(triggers.result)

        return {"type": "notification", "opname": event['owner'],
                "cnotification": {"data": {"datasets": "", "error": messageList}}}