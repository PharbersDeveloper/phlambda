import json
from collections import deque


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


def submitArgsByEngine(curJ, event):
    result = {}
    result['name'] = curJ['name']
    result['type'] = 'spark-submit'
    result['clusterId'] = event['engine']['id']
    result['HadoopJarStep'] = {}
    result['HadoopJarStep']['Jar'] = 'command-runner.jar'

    tmp = []    
    tmp.append('spark-submit')
    tmp.append('--deploy-mode')
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