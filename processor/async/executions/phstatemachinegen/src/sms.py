import json
import os
from collections import deque
from datetime import datetime


def messageAdapter(x):
    x['ll'] = json.loads(x['cmessage'])
    return x


def linearJobWithHooksByJobName(curJ, event, sm, parallelSteps):
    projectName = event['projectName']
    flowVersion = 'developer'
    dagName = '_'.join([projectName, projectName, flowVersion])
    jobName = '_'.join([projectName, projectName, flowVersion, curJ['name']])

    edition = "V2" if os.getenv("EDITION") == "V2" else "dev"
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    # 2. start hook
    sm['States'][curJ['name'] + "StartHook"] = {
        "Type": "Task",
        "Resource": f"arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinejobhook-{edition}:Current",
        "Parameters": {
            "runnerId.$": "$.common.runnerId",
            "projectId.$": "$.common.projectId",
            "projectName.$": "$.common.projectName",
            "owner.$": "$.common.owner",
            "showName.$": "$.common.showName",
            "jobName": curJ["name"],
            "status": "running"

        },
        "ResultPath": None,
        "Next": curJ["name"]
    }
    # 1. job 
    sm['States'][curJ['name']] = {
        "Type": "Task",
        "Resource": "arn:aws-cn:states:::elasticmapreduce:addStep.sync",
        "Parameters": {
            "ClusterId": event['engine']['id'],
            "Step": {
                "Name": curJ['name'],
                "ActionOnFailure": "CONTINUE",
                "HadoopJarStep.$": "$." + curJ['name'] + ".HadoopJarStep"
            }
        },
        "ResultPath": "$.emrRes",
        "Next": curJ["name"] + "LogsCollection",
        "Catch": [ {
             "ErrorEquals": [ "States.Runtime" ],
             "ResultPath": "$.error",
             "Next": curJ["name"] + "FailedLogsParse"
          }, {
             "ErrorEquals": [ "States.TaskFailed" ],
             "ResultPath": "$.error",
             "Next": curJ["name"] + "FailedLogsParse"
          }, {
             "ErrorEquals": [ "States.ALL" ],
             "ResultPath": "$.error",
             "Next": curJ["name"] + "FailedLogsParse"
          } ]
    }

    # 4. logs collections
    sm['States'][curJ['name'] + "LogsCollection"] = {
        "Type": "Task",
        "Resource": "arn:aws-cn:states:::states:startExecution",
        "Parameters": {
            "Input":{
                "common": {
                    "traceId": event["runnerId"],
                    "runnerId": event["runnerId"],
                    "projectId": event["projectId"],
                    "projectName": event["projectName"],
                    "owner": event["owner"],
                    "showName": event["showName"]
                },
                "clusterId": event['engine']['id'],
                "stepId.$": "$.emrRes.Step.Id",
                "jobName": curJ["name"],
                "date": ts
            },
            "StateMachineArn":"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:logs-collection"
        },
        "ResultPath": None,
        "Next": curJ["name"] + "EndHook"
    }

    sm['States'][curJ['name'] + "FailedLogsParse"] = {
        "Type": "Task",
        "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinefailedjobparse-dev",
        "Parameters": {
            "error.$": "$.error"
        },
        "ResultPath": "$.StepId",
        "Next": curJ["name"] + "FailedLogsCollection"
    }

    sm['States'][curJ['name'] + "FailedLogsCollection"] = {
        "Type": "Task",
        "Resource": "arn:aws-cn:states:::states:startExecution",
        "Parameters": {
            "Input":{
                "common": {
                    "traceId": event["runnerId"],
                    "runnerId": event["runnerId"],
                    "projectId": event["projectId"],
                    "projectName": event["projectName"],
                    "owner": event["owner"],
                    "showName": event["showName"]
                },
                "clusterId": event['engine']['id'],
                "stepId.$": "$.StepId",
                "jobName": curJ["name"],
                "date": ts
            },
            "StateMachineArn":"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:logs-collection"
        },
        "ResultPath": None,
        "Next": curJ["name"] + "Failed"
    }

    sm['States'][curJ['name'] + "Failed"] = {
        "Type": "Fail"
    }


    # 3. end hook
    sm['States'][curJ['name'] + "EndHook"] = {
        "Type": "Task",
        "Resource": f"arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinejobhook-{edition}:Current",
        "Parameters": {
            "runnerId.$": "$.common.runnerId",
            "projectId.$": "$.common.projectId",
            "projectName.$": "$.common.projectName",
            "owner.$": "$.common.owner",
            "showName.$": "$.common.showName",
            "stepId.$": "$.emrRes.Step.Id",
            "clusterId": event['engine']['id'],
            "jobName": curJ["name"],
            "status": "success"
        },
        "ResultPath": None
        # "Next": "StateMachineEndHook"
    }


def stack2smdefs(stack, event, sm, prevJobName, parallelSteps=''):
    if len(stack) == 0:
        return

    curJ = stack.pop()

    if len(sm) == 0:
        sm['Comment'] = event['runnerId']
        sm['StartAt'] = ""
        sm['States'] = {
            "StateMachineStartHook": {
                "Type": "Pass"
            }
        }

    if type(curJ) == deque:
        tmpParallelSteps = str(id(curJ))
        sm['States']['Parallel' + tmpParallelSteps] = {
            "Type": "Parallel",
            "InputPath": "$",
            "Branches": [

            ],
            "ResultPath": None,
        }

        index = 0
        for iter in curJ:
            index += 1
            tmpindex = str(index)
            tmpPrevJobName = ''
            tmpsm = {
                'StartAt': '',
                'States': {}
            }

            stack2smdefs(iter, event, tmpsm, tmpPrevJobName, tmpParallelSteps + tmpindex)
            tmpsm['StartAt'] = list(tmpsm['States'].keys())[0]
            # tmpsm['States']['ParalleEndHook' + tmpParallelSteps + tmpindex] = {
            #     "Type": "Pass",
            #     "Result": None,
            #     "End": True
            # }
            sm['States']['Parallel' + tmpParallelSteps]['Branches'].append(tmpsm)

        if 'End' in sm['States'][prevJobName]:
            del sm['States'][prevJobName]['End']
        sm['States'][prevJobName]['Next'] = 'Parallel' + tmpParallelSteps
        prevJobName = 'Parallel' + tmpParallelSteps

    else:
        linearJobWithHooksByJobName(curJ, event, sm, parallelSteps)

        if len(prevJobName) > 0:
            if 'End' in sm['States'][prevJobName]:
                del sm['States'][prevJobName]['End']
            sm['States'][prevJobName]['Next'] = curJ['name'] + 'StartHook'

        # if len(parallelSteps) == 0:
        #     prevJobName = curJ['name'] + 'EndHook'
        prevJobName = curJ['name'] + 'EndHook'

    stack2smdefs(stack, event, sm, prevJobName, parallelSteps)

    if len(prevJobName) > 0 and 'Next' not in sm['States'][prevJobName]:
        # if len(parallelSteps) == 0:
        #     sm['States'][prevJobName]['Next'] = 'StateMachineEndHook'
        # else:
        sm['States'][prevJobName]['End'] = True

    if len(sm['StartAt']) == 0:
        sm['StartAt'] = list(sm['States'].keys())[0]


