import os
import json
import boto3
from datetime import datetime
from collections import deque


def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,  
    jobCat='notification', jobDesc='executionSuccess', message='', status='prepare',
    dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('notification')
    response = table.put_item(
       Item={
            'id': runnerId,
            'projectId': projectId,
            'showName': showName,
            'status': status,
            'jobDesc': jobDesc,
            'comments': comments,
            'message': message,
            'jobCat': jobCat,
            'code': code,
            'category': category,
            'owner': owner
        }
    )
    return response


def dslk2joblk(nldslk, links):
    result = []
    for iter in nldslk:
        nljoblk = list(filter(lambda x: x['ll']['targetName'] == iter['ll']['sourceName'], links))
        # nljoblk = list(filter(lambda x: x['ll']['sourceName'] == iter['ll']['targetName'], links))[0]
        if len(nljoblk) > 0:
            result.append(nljoblk[0])
    return result


def messageAdapter(x):
    x['ll'] = json.loads(x['cmessage'])
    return x


def calDatasetPath(datasetName, datasets, jobs, links, stack):
    dslst = list(filter(lambda x: x['name'] == datasetName, datasets))
    if len(dslst) != 1:
        print(datasetName)
        raise Exception('Wrong Arguments: datasetName')
        return False

    curDs = dslst[0]


    def calNextLevelJob(joblk, nlstack):
        nldataset = list(filter(lambda x: x['name'] == joblk['ll']['targetName'], datasets))
        if len(nldataset) != 1:
            raise Exception('Wrong Arguments: datasetName')
            return False
        calDatasetPath(nldataset[0]['name'], datasets, jobs, links, nlstack)


    llst = list(filter(lambda x: x['ll']['targetName'] == datasetName, links))
    
    if len(llst) == 1:
        # stack.append(llst[0])
        curJ = list(filter(lambda x: x['name'] == llst[0]['ll']['sourceName'], jobs))[0]
        stack.append(curJ)
        nldslk = list(filter(lambda x: x['ll']['targetName'] == llst[0]['ll']['sourceName'], links))
        nljoblk = dslk2joblk(nldslk, links)
        if len(nljoblk) == 1:
            calNextLevelJob(nljoblk[0], stack)
        elif len(nljoblk) > 1:
            cstack = deque()
            for iter in nljoblk:
                tstack = deque()
                tmpJ = list(filter(lambda x: x['name'] == iter['ll']['sourceName'], jobs))[0]
                tstack.append(tmpJ)
                calNextLevelJob(iter, tstack)
                cstack.append(tstack)
            stack.append(cstack)
        else:
            # 递归退出逻辑
            pass

    elif len(llst) > 1:
        raise Exception('Wrong dag: one script only have one output')
        return False
        
    else:
        # 递归退出逻辑
        pass

    return True


def submitArgsByEngine(curJ, event):
    result = {}
    result['name'] = curJ['name']
    result['type'] = 'spark-submit'
    result['clusterId'] = event['engine']['id']
    result['HadoopJarStep'] = {}
    result['HadoopJarStep']['Jar'] = 'command-runner.jar'

    tmp = []    
    tmp.append('spark-submit')
    tmp.append('--depoly-mode')
    tmp.append('cluster')
    tmp.append('--conf')
    tmp.append('spark.driver.cores=1') # To ENV
    tmp.append('--conf')
    tmp.append('spark.driver.memory=1g') # To ENV
    tmp.append('--conf')
    tmp.append('spark.executor.cores=1') # To ENV
    tmp.append('--conf')
    tmp.append('spark.executor.memory=1g') # To ENV
    tmp.append('--conf')
    tmp.append('"spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8"') # To ENV
    tmp.append('--conf')
    tmp.append('"spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8"') # To ENV

    projectName = event['projectName']
    flowVersion = 'developer'
    dagName = '_'.join([projectName, projectName, flowVersion])
    jobName = '_'.join([projectName, projectName, flowVersion, curJ['name']])

    if curJ['runtime'] == 'r' or curJ['runtime'] == 'sparkr':
        tmp.append('--files')
        tmp.append('s3://ph-platform/2020-11-11/jobs/python/phcli/' + dagName + '/' + jobName + '/phjob.R')
        tmp.append('s3://ph-platform/2020-11-11/jobs/python/phcli/' + dagName + '/' + jobName + '/phmain.R')
        tmp.append(event['showName'])
        tmp.append(dagName)
        tmp.append(event['runnerId'])
        tmp.append(jobName)
        tmp.append('job_id_not_implementation')
        tmp.append(event['engine']['dss']['ip'])
        tmp.append(event['calculate']['conf'])
    else:
        tmp.append('--jars')
        tmp.append('s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/clickhouse-jdbc-0.2.4.jar,s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/guava-30.1.1-jre.jar')
        tmp.append('--py-files')
        tmp.append('s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-4.0.0-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/' + dagName + '/' + jobName + '/phjob.py')
        tmp.append('s3://ph-platform/2020-11-11/jobs/python/phcli/' + dagName + '/' + jobName + '/phmain.py')
        tmp.append('--owner')
        tmp.append(event['showName'])
        tmp.append('--dag_name')
        tmp.append(dagName)
        tmp.append('--run_id')
        tmp.append(event['runnerId'])
        tmp.append('--job_full_name')
        tmp.append(jobName)
        tmp.append('--ph_conf')
        tmp.append(event['calculate']['conf'])
    
    result['HadoopJarStep']['Args'] = tmp
    return result


def linearJobWithHooksByJobName(curJ, event, sm, parallelSteps):
    projectName = event['projectName']
    flowVersion = 'developer'
    dagName = '_'.join([projectName, projectName, flowVersion])
    jobName = '_'.join([projectName, projectName, flowVersion, curJ['name']])
    # 2. start hook
    sm['States'][curJ['name'] + "StartHook"] = {
        "Type": "Task",
         "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
         "Parameters": {
            "runnerId.$": "$.common.runnerId",
            "projectId.$": "$.common.projectId",
            "projectName.$": "$.common.projectName",
            "owner.$": "$.common.owner",
            "showName.$": "$.common.showName",
            "jobName": curJ["name"],
            "hook": "start",
            "cat": "step",
            "status": "running"
         },
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
         "Catch": [ {
            "ErrorEquals": [ "States.Runtime" ],
            "ResultPath": "$.error",
            "Next": curJ["name"] + "FailedHook"
         }, {
            "ErrorEquals": [ "States.TaskFailed" ],
            "ResultPath": "$.error",
            "Next": curJ["name"] + "FailedHook"
         }, {
            "ErrorEquals": [ "States.ALL" ],
            "ResultPath": "$.error",
            "Next": curJ["name"] + "FailedHook"
         } ],
         "Next": curJ["name"] + "EndHook"
    }
    # 4. failed hook
    if len(parallelSteps) == 0:
        sm['States'][curJ['name'] + "FailedHook"] = {
            "Type": "Task",
             "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
             "Parameters": {
                "runnerId.$": "$.common.runnerId",
                "projectId.$": "$.common.projectId",
                "projectName.$": "$.common.projectName",
                "owner.$": "$.common.owner",
                "showName.$": "$.common.showName",
                "jobName": curJ["name"],
                "hook": "start",
                "cat": "step",
                "status": "failed"
             },
             "Next": "StateMachineFailedHook"
        }
    else:
        sm['States'][curJ['name'] + "FailedHook"] = {
            "Type": "Task",
             "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
             "Parameters": {
                "runnerId.$": "$.common.runnerId",
                "projectId.$": "$.common.projectId",
                "projectName.$": "$.common.projectName",
                "owner.$": "$.common.owner",
                "showName.$": "$.common.showName",
                "jobName": curJ["name"],
                "hook": "start",
                "cat": "step",
                "status": "failed"
             },
             "Next": "ParalleEndHook" + parallelSteps
        }


    # 3. end hook
    if len(parallelSteps) == 0:
        sm['States'][curJ['name'] + "EndHook"] = {
            "Type": "Task",
             "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
             "Parameters": {
                "runnerId.$": "$.common.runnerId",
                "projectId.$": "$.common.projectId",
                "projectName.$": "$.common.projectName",
                "owner.$": "$.common.owner",
                "showName.$": "$.common.showName",
                "jobName": curJ["name"],
                "hook": "start",
                "cat": "step",
                "status": "success"
             }
             # "Next": "StateMachineEndHook"
        }
    else: 
        sm['States'][curJ['name'] + "EndHook"] = {
            "Type": "Task",
             "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
             "Parameters": {
                "runnerId.$": "$.common.runnerId",
                "projectId.$": "$.common.projectId",
                "projectName.$": "$.common.projectName",
                "owner.$": "$.common.owner",
                "showName.$": "$.common.showName",
                "jobName": curJ["name"],
                "hook": "start",
                "cat": "step",
                "status": "success"
             },
             "Next": "ParalleEndHook" + parallelSteps
        }


def stack2smdefs(stack, event, sm, prevJobName, parallelSteps=''):
    print('===============>')
    print(stack)
    print(prevJobName)
    if len(stack) == 0:
        return

    curJ = stack.popleft()    

    if len(sm) == 0:
        sm['Comment'] = event['runnerId']
        sm['StartAt'] = "StateMachineStartHook"
        sm['States'] = {
            "StateMachineStartHook": {
             "Type": "Task",
             "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
             "Parameters": {
                "runnerId.$": "$.common.runnerId",
                "projectId.$": "$.common.projectId",
                "projectName.$": "$.common.projectName",
                "owner.$": "$.common.owner",
                "showName.$": "$.common.showName",
                "hook": "start",
                "cat": "execute",
                "status": "running"
             },
             "Next": ""
          },
          "StateMachineEndHook": {
             "Type": "Task",
             "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
             "Parameters": {
                "runnerId.$": "$.common.runnerId",
                "projectId.$": "$.common.projectId",
                "projectName.$": "$.common.projectName",
                "owner.$": "$.common.owner",
                "showName.$": "$.common.showName",
                "hook": "end",
                "cat": "execute",
                "status": "success"
             },
             "End": True
          },
          "StateMachineFailedHook": {
             "Type": "Task",
             "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
             "Parameters": {
                "runnerId.$": "$.common.runnerId",
                "projectId.$": "$.common.projectId",
                "projectName.$": "$.common.projectName",
                "owner.$": "$.common.owner",
                "showName.$": "$.common.showName",
                "hook": "end",
                "cat": "execute",
                "status": "failed"
             },
             "End": True
          },
        }

    if type(curJ) == deque:
        parallelSteps = str(id(curJ))
        sm['States']['Parallel' + parallelSteps] = {
            "Type": "Parallel",
            "Branches": [
                
            ],
            "Catch": [ {
                "ErrorEquals": [ "States.Runtime" ],
                "ResultPath": "$.error",
                "Next": "StateMachineFailedHook"
             }, {
                "ErrorEquals": [ "States.TaskFailed" ],
                "ResultPath": "$.error",
                "Next": "StateMachineFailedHook"
             }, {
                "ErrorEquals": [ "States.ALL" ],
                "ResultPath": "$.error",
                "Next": "StateMachineFailedHook"
             } ],   
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

            stack2smdefs(iter, event, tmpsm, tmpPrevJobName, parallelSteps + tmpindex)
            tmpsm['StartAt'] = list(tmpsm['States'].keys())[0]
            tmpsm['States']['ParalleEndHook' + parallelSteps + tmpindex] = {
                "Type": "Task",
                 "Resource": "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phstatemachinehook-dev",
                 "Parameters": {
                    "runnerId.$": "$.common.runnerId",
                    "projectId.$": "$.common.projectId",
                    "projectName.$": "$.common.projectName",
                    "owner.$": "$.common.owner",
                    "showName.$": "$.common.showName",
                    "hook": "end",
                    "cat": "execute",
                    "status": "success"
                 },
                 "End": True
            }
            sm['States']['Parallel' + parallelSteps]['Branches'].append(tmpsm)

        if 'End' in sm['States'][prevJobName]:
            del sm['States'][prevJobName]['End']
        sm['States'][prevJobName]['Next'] = 'Parallel' + parallelSteps
        prevJobName = 'Parallel' + parallelSteps

    else:
        linearJobWithHooksByJobName(curJ, event, sm, parallelSteps)

        if len(prevJobName) > 0:
            if 'End' in sm['States'][prevJobName]:
                del sm['States'][prevJobName]['End']
            sm['States'][prevJobName]['Next'] = curJ['name'] + 'StartHook'

        if len(parallelSteps) == 0:
            prevJobName = curJ['name'] + 'EndHook'
        
    stack2smdefs(stack, event, sm, prevJobName, parallelSteps)
    if len(prevJobName) > 0 and 'Next' not in sm['States'][prevJobName]:
        sm['States'][prevJobName]['Next'] = 'StateMachineEndHook'


def stack2smargs(stack, event, args):
    if len(stack) == 0:
        return

    curJ = stack.popleft()
    # 1. args
    if len(args) == 0:
        common = {}
        common['runnerId'] = event['runnerId']
        common['projectId'] = event['projectId']
        common['projectName'] = event['projectName']
        common['owner'] = event['owner']
        common['showName'] = event['showName']
        args['common'] = common

    if type(curJ) == deque:
        for p in curJ:
            stack2smargs(p, event, args)
    else:
        args[curJ['name']] = submitArgsByEngine(curJ, event)
        stack2smargs(stack, event, args)


def lambda_handler(event, context):
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    dynamodb = boto3.resource('dynamodb')

    # 1. put notification
    put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], dynamodb=dynamodb)
    
    # 2. generator execution args
    # TODO: create args and state machine files
    table = dynamodb.Table('dag')
    items = table.query(
        Select='ALL_ATTRIBUTES',
        Limit=1000,
        ExpressionAttributeValues={
            ':v1': event['projectId']
        },
        KeyConditionExpression='projectId=:v1'
    )['Items']

    datasets = list(filter(lambda x: x['ctype'] == 'node' and x['cat'] == 'dataset', items))
    jobs = list(filter(lambda x: x['ctype'] == 'node' and x['cat'] == 'job', items))
    links = list(filter(lambda x: x['ctype'] == 'link', items))
    links = list(map(messageAdapter, links))
    stackargs = deque()
    stacksm = deque()

    args = {}
    if (calDatasetPath(event['calculate']['name'], datasets, jobs, links, stackargs)):
        stack2smargs(stackargs, event, args)
        
    sm = {}
    if (calDatasetPath(event['calculate']['name'], datasets, jobs, links, stacksm)):
        prevJobName = 'StateMachineStartHook'
        stack2smdefs(stacksm, event, sm, prevJobName)
    
        s3 = boto3.client('s3')
        s3.put_object(
            Body=json.dumps(sm).encode(),
            Bucket='ph-max-auto',
            Key='2020-08-11/' + event['runnerId'] + '.json'
        )
        
        
    return {
        'args': args,
        'sm': 's3://ph-max-auto/2020-08-11/' + event['runnerId'] + '.json'
    }
    