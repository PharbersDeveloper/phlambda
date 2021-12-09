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
    "owner": "hbzhao",
    "start_date": days_ago(1),
    "email": ['airflow@example.com'],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "projectId": "JfSmQBYUpyb4jtest"
}

dag = DAG(
    dag_id="max_test_dag_developer",
    tags=['default'],
    default_args=default_args,
    schedule_interval=None,
    description="A Max Auto Job Example",
    dagrun_timeout=timedelta(minutes=3000.0)
)

default_status = {
    "start": "job开始被调用",
    "end": "job调用结束",
    "error": "job运行失败",
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
            "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-3.0.40-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/phjob.py",
            "s3://ph-platform/2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/phmain.py",
            "--owner", owner,
            "--dag_name", dag_name,
            "--run_id", run_id,
            "--job_full_name", job_full_name,
            "--job_id", "not_implementation"
            ]

    response = s3_client.get_object(
        Bucket="ph-platform",
        Key="2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/args.properties"
    )

    args_str = response["Body"].read().decode()
    args_list = args_str.split("\n")
    deal_args_list=[]
    for arg in args_list:
        if "{{" or "}}" in arg:
            arg = arg.replace("}}", "} }").replace("{{", "{ {")
        deal_args_list.append(arg)

    # 将list转换成dict
    keys = []
    values = []
    for arg in deal_args_list:
        if deal_args_list.index(arg) % 2 == 0:
            keys.append(arg)
        elif deal_args_list.index(arg) % 2 == 1:
            values.append(arg)
    zip_args = zip(keys, values)
    dict_args = dict(zip_args)

    # 获取生成dict中的参数, 将传进来的dict进行替换
    for key in dict_args.keys():
        if key.lstrip('--') in parameters.keys():
            if type(parameters[key.lstrip('--')]) == dict:
                str_args = json.dumps(parameters[key.lstrip('--')], ensure_ascii=False)
                if "{{" or "}}" in str_args:
                    str_args = str_args.replace("}}", "} }").replace("{{", "{ {")
                dict_args[key] = str_args
            elif type(parameters[key.lstrip('--')]) == list:
                list_args = parameters[key.lstrip('--')]
                str_args = json.dumps(list_args)
                dict_args[key] = str_args
            else:
                dict_args[key] = parameters[key.lstrip('--')]

    dict_args.pop("--run_id",None)
    dict_args.pop("--dag_name",None)
    dict_args.pop("--owner",None)
    dict_args.pop("--job_full_name",None)
    dict_args.pop("--job_id",None)

    for key in dict_args.keys():
        args.append(key)
        args.append(dict_args[key])
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

def sync_notification(id, status, job_full_name, run_id):
    data = {}
    data.update({"id": id})
    data.update({"projectId": default_args["projectId"]})
    data.update({"code": "0"})
    data.update({"comments": "<empty>"})
    data.update({"date": str(round(time.time() * 1000))})
    data.update({"jobDesc": "max"})
    message = {
          "type": "notification",
          "opname": default_args["owner"],
          "cnotification": {
              "jobName": job_full_name,
              "runId" : run_id,
              "error": ""
          }
      }
    data.update({"message": json.dumps(message, ensure_ascii=False)})
    data.update({"owner": ""})
    data.update({"showName": default_args["owner"]})
    data.update({"jobCat": status})

    table_name = "notification"
    table = dynamodb_resource.Table(table_name)
    table.put_item(
        Item=data
    )
############## == max_test_dag_developer_test_job_a_bBY0KhVKxA3aFJw == ###################
def max_test_dag_developer_test_job_a_bBY0KhVKxA3aFJw_cmd(**context):

    id = generate()
    dag_name = "max_test_dag_developer"
    job_full_name = "max_test_dag_developer_test_job_a_bBY0KhVKxA3aFJw"
    execution_date = context['ts']
    owner = default_args['owner']
    run_id = dag_name + "_" + execution_date.replace(':', '_')
    job_id = job_full_name + "_" + execution_date.replace(':', '_')
    airflow_run_id = context["dag_run"].run_id.replace(':', '_')
    args = context["dag_run"].conf
    logType = "emr"
    localLog = "S3://ph-platform/logs/airflow/max/" + dag_name + "/" + job_full_name + "/" + execution_date + "/"

    sync_notification(id, default_status.get("start"), job_full_name, run_id)

    try:
        arg_list = create_step_args(run_id, dag_name, job_full_name, owner, args)

        step_message = run_emr_step(dag_name, job_full_name, arg_list)

        res = put_item(run_id, job_id, airflow_run_id, logType, localLog, step_message, lmdLog=None, sfnLog=None)

        status = default_status.get("end")
    except Exception as e:
        status = default_status.get("error") + json.dumps(str(e), ensure_ascii=False)
    finally:
        sync_notification(id, status, job_full_name, run_id)


max_test_dag_developer_test_job_a_bBY0KhVKxA3aFJw = PythonOperator(
    task_id='max_test_dag_developer_test_job_a_bBY0KhVKxA3aFJw',
    provide_context=True,
    python_callable=max_test_dag_developer_test_job_a_bBY0KhVKxA3aFJw_cmd,
    dag=dag
)
############## == max_test_dag_developer_test_job_a_bBY0KhVKxA3aFJw == ###################


max_test_dag_developer_test_job_a_bBY0KhVKxA3aFJw
