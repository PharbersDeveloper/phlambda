import requests
import json
import boto3
import datetime
import traceback


# ssm get url
client = boto3.client('ssm')
response = client.get_parameter(
    Name='airflow_args'
)
ssm_dict = json.loads(response.get("Parameter").get("Value"))


# 运行指定dag
def lambda_handler(event, context):
    msg = eval(event["body"])
    project_name = msg.get("project_name", "max")
    flow_version = msg.get("flow_version", "developer")
    dag_run_id = msg.get("run_id", "ETL_Iterator_ETL_Iterator_developer_2021-12-15T05:09:13+00:00")
    clean_tasks = msg.get("job_name", ["ETL_Iterator_ETL_Iterator_developer_compute_vvv_r1cjJ3Kz7yGyLv1"])
    is_down_stream = msg.get("down_stream", "false")
    execution_date = dag_run_id[dag_run_id.rfind("_")+1:]
    dag_id = "_".join([project_name, project_name, flow_version])

    if project_name in ["default", "max"]:
        url = ssm_dict.get(project_name)
    else:
        url = ssm_dict.get("max")
    print(url)

    res = {}
    headers = {
        # "Authorization": 'Basic Base64(webuser:password)',
        "Content-type": 'application/json',
        "Accept": 'application/json'
    }

    # 如果存在dag_id将状态改为激活
    # https://airflow.apache.org/api/v1/dags/{dag_id}/updateTaskInstancesState
    # https://airflow.apache.org/api/v1/dags/{dag_id}/clearTaskInstances
    url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/clearTaskInstances"
    # url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/updateTaskInstancesState"
    # url = "http://" + url + "/api/v1/dags/" + dag_id
    try:
        # body = {
        #     "dry_run": True,
        #     "task_id": clean_tasks[0],
        #     "include_future": False,
        #     "include_past": False,
        #     "include_upstream": True,
        #     "include_downstream": True,
        #     "new_state": "success",
        #     "execution_date": execution_date
        # }
        body = {
            "dry_run": False,
            "task_ids": clean_tasks,
            "start_date": execution_date,
            "end_date": execution_date,
            "only_failed": True,
            "only_running": False,
            "include_subdags": True,
            "include_parentdag": True,
            "reset_dag_runs": True
        }
        result = requests.post(url=url, data=json.dumps(body), headers=headers)

        tmp = result.json()['task_instances']
        dag_id = tmp[0]['dag_id']
        dag_run_id = tmp[0]['dag_run_id']
        dag_task_id = tmp[0]['task_id']

        # url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/dagRuns/" + dag_run_id + "/taskInstances/" + dag_task_id
        # result = requests.get(url=url, headers=headers)


        if result.status_code != 200:
            res["status"] = "failed"
            res["msg"] = dag_id + " Activation failed"

    except:
        print(traceback.format_exc())
        res["status"] = "failed"
        res["msg"] = url + "api error"

    # dag_id状态激活后即可开始run
    # runs_url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/dagRuns"
    # runs_url = "http://" + url + "/api/v1/dags/" + dag_id + "/dagRuns"


    return {
        "headers": { "Access-Control-Allow-Origin": "*"},
        "statusCode": 200 if res["status"] == "success" else 502,
        "body": json.dumps(res)
    }
