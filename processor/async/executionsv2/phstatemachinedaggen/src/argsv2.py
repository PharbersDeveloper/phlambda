import json
import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')


def get_dagcof_item_by_jobId(projectId, jobId):

    ds_table = dynamodb.Table('dagconf')
    res = ds_table.query(
        IndexName='dagconf-projectId-id-indexd',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("id").eq(jobId)
    )
    return res["Items"][0]


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
    coefficient = event['calculate']['conf']['userConf'].get("coefficient", "1")
    # print("====================================>>>>start")
    # print(event['calculate']['conf'])

    spark_args = {
        "1": {
            "SPARK_DRIVER_CORES": "1",
            "SPARK_DRIVER_MEMORY": "1g",
            "SPARK_EXECUTOR_CORES": "1",
            "SPARK_EXECUTOR_MEMORY": "1g"
        },
        "2": {
            "SPARK_DRIVER_CORES": "1",
            "SPARK_DRIVER_MEMORY": "2g",
            "SPARK_EXECUTOR_CORES": "1",
            "SPARK_EXECUTOR_MEMORY": "2g"
        },
        "3": {
            "SPARK_DRIVER_CORES": "2",
            "SPARK_DRIVER_MEMORY": "2g",
            "SPARK_EXECUTOR_CORES": "2",
            "SPARK_EXECUTOR_MEMORY": "2g"
        },
        "4": {
            "SPARK_DRIVER_CORES": "2",
            "SPARK_DRIVER_MEMORY": "4g",
            "SPARK_EXECUTOR_CORES": "2",
            "SPARK_EXECUTOR_MEMORY": "4g"
        },
        "5": {
            "SPARK_DRIVER_CORES": "4",
            "SPARK_DRIVER_MEMORY": "4g",
            "SPARK_EXECUTOR_CORES": "4",
            "SPARK_EXECUTOR_MEMORY": "4g"
        }

    }
    # print("====================================>>>>end")
    tmp = []
    tmp.append('spark-submit')
    tmp.append('--deploy-mode')
    tmp.append('cluster')
    tmp.append('--conf')
    tmp.append('spark.driver.cores=' + spark_args[coefficient]["SPARK_DRIVER_CORES"])  # To ENV
    tmp.append('--conf')
    tmp.append('spark.driver.memory=' + spark_args[coefficient]["SPARK_DRIVER_MEMORY"])  # To ENV
    tmp.append('--conf')
    tmp.append('spark.executor.cores=' + spark_args[coefficient]["SPARK_EXECUTOR_CORES"])  # To ENV
    tmp.append('--conf')
    tmp.append('spark.executor.memory=' + spark_args[coefficient]["SPARK_EXECUTOR_MEMORY"])  # To ENV
    tmp.append('--conf')
    tmp.append('spark.executor.extraJavaOptions=%s' % (os.getenv("SPARK_EXECUTOR_EXTRAJAVAOPTIONS")))  # To ENV
    tmp.append('--conf')
    tmp.append('spark.driver.extraJavaOptions=%s' % (os.getenv("SPARK_EXECUTOR_EXTRAJAVAOPTIONS")))  # To ENV
    tmp.append('--conf')
    tmp.append('spark.sql.broadcastTimeout=%s' % (os.getenv("SPARK_SQL_BROADCASTTIMEOUT")))  # To ENV
    tmp.append('--conf')
    tmp.append('spark.sql.autoBroadcastJoinThreshold=%s' % (os.getenv("SPARK_SQL_AUTOBROADCASTJOINTHRESHOLD")))  # To ENV
    # TODO: 注释掉的原因是，小鹿那边需要下载文件去做验证，还得reparation为1个去下载
    # tmp.append('--conf')
    # tmp.append(f"spark.sql.files.maxRecordsPerFile={os.getenv('SPARK_FILE_MAX_RECORDS')}")

    projectName = event['projectName']
    projectIp = event['engine']['dss']['ip']
    flowVersion = 'developer'
    dagName = '_'.join([projectName, projectName, flowVersion])
    jobName = '_'.join([projectName, projectName, flowVersion, curJ['name']])
    # 通过projecId
    projectId = event["projectId"]
    jobId = curJ["representId"]
    inputs = json.loads(get_dagcof_item_by_jobId(projectId, jobId)["inputs"])
    datasets = event['calculate']['conf']['datasets']
    input_datasets = []
    for dataset in datasets:
        if dataset["name"] in inputs:
            print(dataset["name"])
            input_datasets.append(dataset)
    dict_ph_conf = event['calculate']['conf'].copy()
    dict_ph_conf["datasets"] = input_datasets

    ph_conf = json.dumps(dict_ph_conf, ensure_ascii=False).replace("}}", "} }").replace("{{", "{ {")
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