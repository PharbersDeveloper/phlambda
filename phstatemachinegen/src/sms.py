import json
from collections import deque


def messageAdapter(x):
    x['ll'] = json.loads(x['cmessage'])
    return x


def linearJobWithHooksByJobName(curJ, event, sm, parallelSteps):
    projectName = event['projectName']
    flowVersion = 'developer'
    dagName = '_'.join([projectName, projectName, flowVersion])
    jobName = '_'.join([projectName, projectName, flowVersion, curJ['name']])

    # 2. start hook
    sm['States'][curJ['name'] + "StartHook"] = {
        "Type": "Task",
        "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinejobhook-dev:Current",
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
        "ResultPath": None,
        "Next": curJ["name"] + "EndHook"
    }

    # 3. end hook
    sm['States'][curJ['name'] + "EndHook"] = {
        "Type": "Task",
        "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinejobhook-dev:Current",
        "Parameters": {
            "runnerId.$": "$.common.runnerId",
            "projectId.$": "$.common.projectId",
            "projectName.$": "$.common.projectName",
            "owner.$": "$.common.owner",
            "showName.$": "$.common.showName",
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


