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


def updateTaskInstancesState(project_name, dag_id, task_id, execution_date, is_downstream, is_upstream):
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    # 1. 第一步先全部改成success, 这样做的原因在于，将所有的下线全部统一一个状态
    # url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/clearTaskInstances"
    airflow_url = ssm_dict.get(project_name)
    url = "http://" + airflow_url + "/api/v1/dags/" + dag_id + "/updateTaskInstancesState"
    print("updateTaskInstancesState url")
    print(url)
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


def clearTaskInstances(project_name, dag_id, clean_tasks, execution_date):
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    airflow_url = ssm_dict.get(project_name)
    url = "http://" + airflow_url + "/api/v1/dags/" + dag_id + "/clearTaskInstances"
    print("clearTaskInstances的 url")
    print(url)
    # url = "http://" + url + "/api/v1/dags/" + dag_id
    body = {
        "dry_run": False,
        "task_ids": clean_tasks,
        "start_date": execution_date,
        "end_date": execution_date,
        "only_failed": False,
        "only_running": False,
        "include_subdags": True,
        "include_parentdag": True,
        "reset_dag_runs": True
    }
    print(body)
    result = requests.post(url=url, data=json.dumps(body), headers=headers)
    print(result)
    if result.status_code != 200:
        raise Exception()

    return


def delete_dy_item(item):
    run_id = item["run_id"]
    task_ids = item["task_ids"]
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table("notification")
    for tid in task_ids:
        table.delete_item(
            Key = {
                "id": run_id,
                "projectId": tid
            }
        )


# 运行指定dag
def lambda_handler(event, context):
    msg = eval(event["body"])
    print("输入参数")
    print(msg)
    project_name = msg.get("project_name", "max")
    print(project_name)
    flow_version = msg.get("flow_version", "developer")
    dag_run_id = msg.get("run_id", "ETL_Iterator_ETL_Iterator_developer_2021-12-15T05:09:13+00:00")
    print(dag_run_id)
    task_id = msg.get("task_id", "ETL_Iterator_ETL_Iterator_developer_compute_vvv_r1cjJ3Kz7yGyLv1")
    execution_date = dag_run_id[dag_run_id.rfind("_") + 1:]
    dag_id = "_".join([project_name, project_name, flow_version])
    clear_task_cat = msg.get("clean_cat", "self_only")  # self_only, upstream, downstream

    print("进入retry流程1148")
    try:
        clean_tasks = [task_id]

        if clear_task_cat != "self_only":
            clean_tasks = updateTaskInstancesState(project_name, dag_id, task_id, execution_date,
                                                   is_upstream=True if clear_task_cat == "upstream" else False,
                                                   is_downstream=True if clear_task_cat == "downstream" else False)

        print("clean的task")
        print(clean_tasks)
        delete_dy_item({
            "run_id": dag_run_id,
            "task_ids": clean_tasks
        })
        print()
        clearTaskInstances(project_name, dag_id, clean_tasks, execution_date)
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
        print(str(e))
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
