import os
import json
import boto3
import traceback
import time
from datetime import datetime
from exceptions import ScenarioResourceError
from exceptions import ScenarioStackNotExistError


def getStackExisted(cf, stackName):
    try:
        stacks = cf.describe_stacks(StackName=stackName)['Stacks']
        if len(stacks) > 0:
            return stacks[0]
    except Exception:
        raise ScenarioStackNotExistError('stack not exist error')


def checkStackStatus(cf, stack):
    print('check status ============>')
    print(stack['StackStatus'])
    if stack['StackStatus'] != "UPDATE_COMPLETE" and stack['StackStatus'] != "CREATE_COMPLETE":
        raise ScenarioResourceError('stack is updating or createing, please update later')


def checkNeedUpdateResouce(cf, stack, checkDict):
    params = stack['Parameters']
    result = False
    for item in params:
        result |= item['ParameterValue'] != checkDict[item['ParameterKey']]

    return result


def scenarioCUProcessor(tenantId, targetArn, projectId, scenarioId, triggerId, cronExpression):
    result = {}
    dt = datetime.now() 
    date = dt.strftime('%Y-%m-%d-%H-%M-%S')

    cf = boto3.client('cloudformation')
    stackName = "-".join(["scenario", projectId, scenarioId, triggerId])
    changeSetName = "-".join([stackName, date])

    try:
        stack = getStackExisted(cf, stackName)
        print(stack)
        checkDict = {
            "BusName": "default",
            "ScheduleExpression": cronExpression,
            "TenantId": tenantId,
            "ScenarioId": scenarioId,
            "TriggerId": triggerId,
            "ProjectId": projectId,
            "TargetArn": targetArn,
            "TimerName": stackName
        }

        checkStackStatus(cf, stack)
        if (checkNeedUpdateResouce(cf, stack, checkDict)):
            response = cf.create_change_set(
                StackName=stackName,
                ChangeSetName=changeSetName,
                TemplateURL='https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/jobs/statemachine/pharbers/template/scenario-timer-cfn.yaml',
                Parameters=[
                    {
                        "ParameterKey": "TimerName",
                        "ParameterValue": stackName
                    },
                    {
                        "ParameterKey": "ScheduleExpression",
                        "ParameterValue": cronExpression
                    },
                    {
                        "ParameterKey": "TenantId",
                        "ParameterValue": tenantId
                    },
                    {
                        "ParameterKey": "ScenarioId",
                        "ParameterValue": scenarioId
                    },
                    {
                        "ParameterKey": "TriggerId",
                        "ParameterValue": triggerId
                    },
                    {
                        "ParameterKey": "ProjectId",
                        "ParameterValue": projectId
                    },
                ]
            )
            print(response)


            while True:
                time.sleep(2)
                response = cf.describe_change_set(
                    ChangeSetName=changeSetName,
                    StackName=stackName
                )
                print(response)

                if response['Status'] == 'CREATE_COMPLETE':
                    break


            cf.execute_change_set(
                ChangeSetName=changeSetName,
                StackName=stackName
            )
            result['status'] = 'ok'
            result['message'] = 'updating resource'

    except ScenarioStackNotExistError:
        print('create stack trigger ==============>')
        print(cf)
        response = cf.create_stack(
            StackName=stackName,
            TemplateURL='https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/jobs/statemachine/pharbers/template/scenario-timer-cfn.yaml',
            Parameters=[
                {
                    "ParameterKey": "TimerName",
                    "ParameterValue": stackName
                },
                {
                    "ParameterKey": "ScheduleExpression",
                    "ParameterValue": cronExpression
                },
                {
                    "ParameterKey": "TenantId",
                    "ParameterValue": tenantId
                },
                {
                    "ParameterKey": "ScenarioId",
                    "ParameterValue": scenarioId
                },
                {
                    "ParameterKey": "TriggerId",
                    "ParameterValue": triggerId
                },
                {
                    "ParameterKey": "ProjectId",
                    "ParameterValue": projectId
                },
            ]
        )
        print(response)

        # while True:
        #     time.sleep(2)
        #     response = client.describe_stacks(
        #         StackName=stackName #  event['runnerId']
        #     )
        #     print(response)

        #     if len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] == 'CREATE_COMPLETE':
        #         break

        result['status'] = 'ok'
        result['message'] = 'create resource'

    except ScenarioResourceError as e:
        traceback_output = traceback.format_exc()
        print(traceback_output)
        result['status'] = 'error'
        result['message'] = str(e)

    except Exception:
        print('unknown error ===========>')
        traceback_output = traceback.format_exc()
        print(traceback_output)
    finally:
        return result