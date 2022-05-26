import json
import os

def extractJobArgs(jobNames, jobs, event):
    args = {}

    common = {}
    common['runnerId'] = event['runnerId']
    common['projectId'] = event['projectId']
    common['projectName'] = event['projectName']
    common['owner'] = event['owner']
    common['showName'] = event['showName']
    args['common'] = common

    for n in jobNames:
        curJ = list(filter(lambda x: x["name"] == n, jobs))[0]
        args[n] = submitArgsByEngine(curJ, event)

    return args


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
    # tmp.append('--conf')
    # tmp.append('spark.driver.cores=' + os.getenv("SPARK_DRIVER_CORES")) # To ENV
    # tmp.append('--conf')
    # tmp.append('spark.driver.memory=' + os.getenv("SPARK_DRIVER_MEMORY")) # To ENV
    # tmp.append('--conf')
    # tmp.append('spark.executor.cores=' + os.getenv("SPARK_EXECUTOR_CORES")) # To ENV
    # tmp.append('--conf')
    # tmp.append('spark.executor.memory=' + os.getenv("SPARK_EXECUTOR_MEMORY")) # To ENV
    tmp.append('--conf')
    tmp.append('spark.executor.extraJavaOptions=%s' % (os.getenv("SPARK_EXECUTOR_EXTRAJAVAOPTIONS"))) # To ENV
    tmp.append('--conf')
    tmp.append('spark.driver.extraJavaOptions=%s' % (os.getenv("SPARK_EXECUTOR_EXTRAJAVAOPTIONS"))) # To ENV

    projectName = event['projectName']
    projectIp = event['engine']['dss']['ip']
    flowVersion = 'developer'
    dagName = '_'.join([projectName, projectName, flowVersion])
    jobName = '_'.join([projectName, projectName, flowVersion, curJ['name']])
    ph_conf = json.dumps(event['calculate']['conf'], ensure_ascii=False).replace("}}", "} }").replace("{{", "{ {")

    if curJ['runtime'] == 'r' or curJ['runtime'] == 'sparkr':
        tmp.append('--jars')
        tmp.append('/jars/clickhouse-jdbc-0.2.4.jar,/jars/guava-30.1.1-jre.jar')
        tmp.append('--files')
        tmp.append('s3://ph-platform/2020-11-11/jobs/python/phcli/' + dagName + '/' + jobName + '/phjob.R')
        tmp.append('s3://ph-platform/2020-11-11/jobs/python/phcli/' + dagName + '/' + jobName + '/phmain.R')
        tmp.append(event['showName'])
        tmp.append(dagName)
        tmp.append(event['runnerId'])
        tmp.append(jobName)
        tmp.append('job_id_not_implementation')
        tmp.append(projectIp)
        tmp.append(ph_conf)
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
        tmp.append('--project_ip')
        tmp.append(projectIp)
        tmp.append('--ph_conf')
        tmp.append(ph_conf)

    result['HadoopJarStep']['Args'] = tmp
    return result

