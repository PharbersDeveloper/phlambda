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


def updateTaskInstancesState(dag_id, task_id, execution_date, is_downstream, is_upstream):
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    # 1. 第一步先全部改成success, 这样做的原因在于，将所有的下线全部统一一个状态
    # url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/clearTaskInstances"
    url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/updateTaskInstancesState"
    # url = "http://" + url + "/api/v1/dags/" + dag_id
    body = {
        "dry_run": False,
        "task_id": task_id,
        "include_future": False,
        "include_past": False,
        "include_upstream": is_upstream,
        "include_downstream": is_downstream,
        "new_state": "success",
        "execution_date": execution_date
    }

    result = requests.post(url=url, data=json.dumps(body), headers=headers)
    if result.status_code != 200:
        raise Exception()

    # 2. 第一步先全部改成failed, 这样做的原因在于, 能一次性得到所有的下线或上线的task_id
    body = {
        "dry_run": False,
        "task_id": task_id,
        "include_future": False,
        "include_past": False,
        "include_upstream": is_upstream,
        "include_downstream": is_downstream,
        "new_state": "failed",
        "execution_date": execution_date
    }
    result = requests.post(url=url, data=json.dumps(body), headers=headers)
    if result.status_code != 200:
        raise Exception()

    task_instances = result.json()['task_instances']
    reVal = []
    for ins in task_instances:
        reVal.append(ins["task_id"])

    print(reVal)
    return reVal


def clearTaskInstances(dag_id, clean_tasks, execution_date):
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/clearTaskInstances"
    # url = "http://" + url + "/api/v1/dags/" + dag_id
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
    if result.status_code != 200:
        raise Exception()

    return


# 运行指定dag
def lambda_handler(event, context):
    msg = eval(event["body"])
    project_name = msg.get("project_name", "max")
    flow_version = msg.get("flow_version", "developer")
    dag_run_id = msg.get("run_id", "ETL_Iterator_ETL_Iterator_developer_2021-12-15T05:09:13+00:00")
    task_id = msg.get("task_id", "ETL_Iterator_ETL_Iterator_developer_compute_vvv_r1cjJ3Kz7yGyLv1")
    execution_date = dag_run_id[dag_run_id.rfind("_") + 1:]
    dag_id = "_".join([project_name, project_name, flow_version])
    clear_task_cat = msg.get("clean_cat", "self_only")  # self_only, upstream, downstream

    if project_name in ["default", "max"]:
        url = ssm_dict.get(project_name)
    else:
        url = ssm_dict.get("max")
    print(url)

    try:
        clean_tasks = [task_id]
        if clear_task_cat != "self_only":
            clean_tasks = updateTaskInstancesState(dag_id, task_id, execution_date,
                                                   is_upstream=clear_task_cat == "upstream",
                                                   is_downstream=clear_task_cat == "downstream")

        clearTaskInstances(dag_id, clean_tasks, execution_date)
        res = {
            "status": "success",
            "data": {
                "execution_date": execution_date,
                "project_name": project_name,
                "flow_version": flow_version,
                "task_id": task_id,
                "clean_cat": clear_task_cat
            }
        }
    except Exception as e:
        res = {
            "status": "error",
            "data": {
                "execution_date": execution_date,
                "project_name": project_name,
                "flow_version": flow_version,
                "task_id": task_id,
                "clean_cat": clear_task_cat
            },
            "message": "something wrong"
        }

    return {
        "headers": {"Access-Control-Allow-Origin": "*"},
        "statusCode": 200 if res["status"] == "success" else 502,
        "body": json.dumps(res)
    }
