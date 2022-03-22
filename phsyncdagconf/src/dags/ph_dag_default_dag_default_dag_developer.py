import os
import uuid
import time
import json
import boto3
import math
import random
import string
import datetime
import subprocess
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.models import DAG, Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

emr_client = boto3.client('emr')
s3_client = boto3.client('s3')
dynamodb_resource = boto3.resource("dynamodb")
ACTIONONFAILURE = "CONTINUE"
STEP_JAR = "command-runner.jar"

default_args = {
    "owner": "default_owner",
    "showName": "default_showName",
    "start_date": days_ago(1),
    "email": ['airflow@example.com'],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "projectId": "default_projectId"
}

dag = DAG(
    dag_id="default_dag_default_dag_developer",
    tags=['default'],
    default_args=default_args,
    schedule_interval=None,
    description="A Max Auto Job Example",
    dagrun_timeout=timedelta(minutes=3000.0)
)

default_status = {
    "start": "running",
    "end": "success",
    "error": "failed",
}

var_key_lst = Variable.get("%s__SPARK_CONF" % (dag.dag_id), deserialize_json=True, default_var={})

# subprocess Ponen CMD
def process_cmd(cmd):
    print("process: " + cmd)

    p = subprocess.Popen(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    last_line = ''
    while p.poll() is None:
        line = p.stdout.read().strip("\n")
        if line:
            last_line = line
            print(last_line)
    if p.returncode == 0:
        print('Subprogram success')
    else:
        raise Exception(last_line)

def create_step_args(run_id, dag_name, job_full_name, owner, parameters):

    args = ["spark-submit",
            "--deploy-mode", "cluster",
            "--conf", "spark.driver.cores=1",
            "--conf", "spark.driver.memory=1g",
            "--conf", "spark.executor.cores=1",
            "--conf", "spark.executor.memory=1g",
            "--conf", "spark.executor.instances=1",
            "--conf", "spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
            "--conf", "spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
            "--jars", "s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/clickhouse-jdbc-0.2.4.jar,s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/guava-30.1.1-jre.jar",
            "--py-files",
            "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-4.0.0-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/phjob.py",
            "s3://ph-platform/2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/phmain.py",
            "--owner", owner,
            "--dag_name", dag_name,
            "--run_id", run_id,
            "--job_full_name", job_full_name,
            "--ph_conf", json.dumps(parameters, ensure_ascii=False).replace("}}", "} }").replace("{{", "{ {"),
            "--job_id", "not_implementation"
            ]

    return args

def get_cluster_id():
    res = emr_client.list_clusters(
        ClusterStates=[
            "WAITING",
            "RUNNING"
        ]
    )
    cluster_ids = list([cluster['Id'] for cluster in res.get('Clusters') if cluster['Name'] =="phdev"])
    return cluster_ids[0]

def run_emr_step(dag_name, job_full_name, args_list=None):
    cluster_id = get_cluster_id()
    step_name = dag_name + "_" + job_full_name

    step = {}
    step.update({"Name": step_name})
    step.update({"ActionOnFailure": ACTIONONFAILURE})
    step.update({"HadoopJarStep": {}})
    step["HadoopJarStep"].update({"Jar": STEP_JAR})
    step["HadoopJarStep"].update({"Args": args_list})
    steps=[]
    steps.append(step)
    run_step_response = emr_client.add_job_flow_steps(
        JobFlowId=cluster_id,
        Steps=steps
    )

    while run_step_response:
        time.sleep(30)
        step_information_response = emr_client.describe_step(
            ClusterId=cluster_id,
            StepId=run_step_response["StepIds"][0]
        )
        step_statuses = ["COMPLETED", "FAILED", "CANCELLED", "INTERRUPTED"]

        if step_information_response['Step']['Status']['State'] in step_statuses:
            step_id = run_step_response["StepIds"][0]
            step_status = step_information_response['Step']['Status']['State']
            break

    emr_log = "s3://ph-platform/2020-11-11/emr/logs/" + cluster_id + "/steps/" + step_id + "/"

    return {
        "emr_log": emr_log,
        "step_status": step_status
    }

def put_item(run_id, job_id, airflowRunId, logType, localLog, step_message, lmdLog=None ,sfnLog=None):
    data={}
    data.update({"runId": run_id})
    data.update({"jobId": job_id})
    data.update({"airflowRunId": airflowRunId})
    data.update({"logType": logType})
    data.update({"localLog": localLog})
    data.update({"emrLog": step_message.get("emr_log")})
    data.update({"lmdLog": lmdLog})
    data.update({"sfnLog": sfnLog})

    table_name = "logs"
    table = dynamodb_resource.Table(table_name)
    table.put_item(
        Item=data
    )

    if step_message.get("step_status") == "FAILED" or step_message.get("step_status") == "CANCELLED":
        raise Exception ("job 运行出错")
    return {
        "data": data
    }

def get_dy_item(table_name, key):
    table = dynamodb_resource.Table(table_name)
    res = table.get_item(
        Key=key,
    )

    return res.get("Item")

def generate():
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
              "abcdefghijklmnopqrstuvwxyz" \
              "0123456789-_"

    charsetLength = len(charset)
    keyLength = 3 * 5

    array = []
    for i in range(keyLength):
        array.append(charset[math.floor(random.random() * charsetLength)])

    return "".join(array)

def sync_notification(id, status, job_full_name, run_id, job_show_name):
    data = {}
    data.update({"id": run_id})
    data.update({"projectId": job_full_name})
    data.update({"code": "0"})
    data.update({"comments": "<empty>"})
    data.update({"date": str(round(time.time() * 1000))})
    data.update({"jobDesc": "max"})
    message = {
          "type": "notification",
          "opname": default_args["owner"],
          "projectId": default_args["projectId"],
          "cnotification": {
              "jobName": job_full_name,
              "runId" : run_id,
              "jobShowName" : job_show_name,
              "error": ""
          }
      }
    data.update({"message": json.dumps(message, ensure_ascii=False)})
    data.update({"owner": default_args["owner"]})
    data.update({"showName": default_args["showName"]})
    data.update({"jobCat": status})

    table_name = "notification"
    table = dynamodb_resource.Table(table_name)
    table.put_item(
        Item=data
    )

def sync_executionStatus(id, current_status, job_full_name, execution_date, run_id, args):
    table_name = "executionStatus"
    data = {}
    projectId = default_args.get("projectId")
    ownerId = args.get("ownerId", default_args.get("owner"))
    data.update({"id": projectId + "_" + ownerId})
    data.update({"date": execution_date})
    data.update({"runnerId": run_id})
    data.update({"current": job_full_name})
    key = {
        "id": projectId + "_" + ownerId,
        "date": execution_date
    }
    item = get_dy_item(table_name, key)
    dag_status = "default_dag_status"
    if item:
        dag_status = item.get("status")
    # 如果current_status和dynamodb中status相与一个failed status为failed
    # 如果current_status为 running dynamodb为 running,success status为running
    # 如果current_status为 success dynamodb为 success,running status为 success
    if dag_status == "failed":
        current_status = "failed"
    data.update({"status": current_status})

    table = dynamodb_resource.Table(table_name)
    table.put_item(
        Item=data
    )
############## == default_dag_default_dag_developer_default_job_a == ###################
def default_dag_default_dag_developer_default_job_a_cmd(**context):

    id = generate()
    dag_name = "default_dag_default_dag_developer"
    job_full_name = "default_dag_default_dag_developer_default_job_a"
    job_show_name = "default_job_a"
    execution_date = context['ts']
    owner = default_args['owner']
    showName = default_args['showName']
    run_id = dag_name + "_" + execution_date
    job_id = job_full_name
    airflow_run_id = context["dag_run"].run_id
    args = context["dag_run"].conf
    logType = "emr"
    localLog = "S3://ph-platform/logs/airflow/default_dag/" + dag_name + "/" + job_full_name + "/" + execution_date + "/"

    # sync_notification(id, default_status.get("start"), job_full_name, run_id, args)
    # sync_executionStatus(id, default_status.get("start"), job_full_name, execution_date, run_id, args)

    try:
        arg_list = create_step_args(run_id, dag_name, job_full_name, showName, args)

        step_message = run_emr_step(dag_name, job_full_name, arg_list)

        res = put_item(run_id, job_id, airflow_run_id, logType, localLog, step_message, lmdLog=None, sfnLog=None)

        status = default_status.get("end")
    except Exception as e:
        status = default_status.get("error")
        raise e
    # finally:
        # sync_notification(id, status, job_full_name, run_id, args)
        # sync_executionStatus(id, status, job_full_name, execution_date, run_id, args)


default_dag_default_dag_developer_default_job_a = PythonOperator(
    task_id='default_dag_default_dag_developer_default_job_a',
    provide_context=True,
    python_callable=default_dag_default_dag_developer_default_job_a_cmd,
    dag=dag
)
############## == default_dag_default_dag_developer_default_job_a == ###################


default_dag_default_dag_developer_default_job_a
