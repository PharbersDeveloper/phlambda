import boto3
import time
import re

def lambda_handler(event, context):

    glue_job_name = 'cols-modification'
    arguments = event['parameter']['args']

    glue_client = boto3.client('glue')

    run_response = glue_client.start_job_run(
        JobName=glue_job_name,
        Arguments=arguments
    )

    glue_job_run_id = run_response['JobRunId']

    while True:
        response = glue_client.get_job_run(
            JobName=glue_job_name,
            RunId=glue_job_run_id
        )
        if response['JobRun']['JobRunState'] == 'SUCCEEDED':
            break
        if response['JobRun']['JobRunState'] == 'FAILED':
            raise Exception("GlueJob运行失败")
            break
        if response['JobRun']['JobRunState'] == 'TIMEOUT':
            raise Exception("GlueJob运行超时")
            break
        if response['JobRun']['JobRunState'] == 'STOPPED':
            raise Exception("GlueJob运行停止")
            break
        time.sleep(60)

    file = arguments['file']
    bucket = arguments['bucket']
    version = arguments['version']
    sheet = arguments['sheet']
    table = arguments['table']
    reg = ".xlsx"

    if version == file.split(".")[0] + "_" + sheet:
        output = re.sub(reg, "", file + "_" + sheet + ".csv")
    else:
        output = re.sub(reg, "", file + "_" + sheet + "_" + version + ".csv")

    p_input = "s3://" + bucket + "/2020-11-11/etl/temporary_csv/" + table + "/" + output
    p_output = "s3://" + bucket + "/2020-11-11/etl/readable_files/" + table

    parameter = {"p_input": "", "p_output": "", "g_partition": "provider, version", "g_filldefalut": "NONE", "g_bucket": "NONE", "g_mapping": "NONE"}
    parameter['p_input'] = p_input
    parameter['p_output'] = p_output

    args = ["spark-submit",
            "--deploy-mode", "cluster",
            "--conf", "spark.driver.cores=1",
            "--conf", "spark.driver.memory=1g",
            "--conf", "spark.executor.cores=1",
            "--conf", "spark.executor.memory=1g",
            "--conf", "spark.executor.instances=1",
            "--conf", "spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
            "--conf", "spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
            "--py-files",
            "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-3.0.7-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/readable/for_readable_move_to_readable/phjob.py",
            "s3://ph-platform/2020-11-11/jobs/python/phcli/readable/for_readable_move_to_readable/phmain.py",
            "--owner", "default_owner",
            "--dag_name", "readable",
            "--run_id", "readable_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()),
            "--job_full_name", "for_readable_move_to_readable",
            "--job_id", "not_implementation"
            ]

    for key in parameter.keys():
        args.append("--" + key)
        args.append(parameter[key])

    return {
        "args" : args
    }