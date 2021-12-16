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
    conf = msg.get("conf", {})
    dag_id = "_".join([project_name, project_name, flow_version])

    if project_name in ["default", "max"]:
        url = ssm_dict.get(project_name)
    else:
        url = ssm_dict.get("max")
    print(url)

    res = {}
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }

    # 如果存在dag_id将状态改为激活
    # update_url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id
    update_url = "http://" + url + "/api/v1/dags/" + dag_id
    try:
        body = {"is_paused": False}
        result = requests.patch(url=update_url, data=json.dumps(body), headers=headers)
        if result.status_code != 200:
            res["status"] = "failed"
            res["msg"] = dag_id + " Activation failed"

    except:
        res["status"] = "failed"
        res["msg"] = update_url + "api error"

    # dag_id状态激活后即可开始run
    # runs_url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/dagRuns"
    runs_url = "http://" + url + "/api/v1/dags/" + dag_id + "/dagRuns"

    try:
        execution_date = datetime.datetime.utcnow()
        # dag_run_id = "_".join([project_name, dag_id, flow_version])
        dag_run_id = "_".join([project_name, project_name, flow_version, execution_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")])
        body = {
            "dag_run_id": dag_run_id,
            "execution_date": execution_date.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "conf": conf
        }
        dag_runs = requests.post(url=runs_url, data=json.dumps(body), headers=headers)
        if dag_runs.status_code == 200:
            airflow_result = dag_runs.json()
            res["status"] = "success"
            res["data"] = {
                "dag_run_id": airflow_result["dag_run_id"],
                "dag_id": airflow_result["dag_id"],
                "run_id": dag_run_id,
                "project_name": project_name
            }
        else:
            res["status"] = "failed"
            res["msg"] = dag_id + " Trigger failure"

    except:
        print(traceback.format_exc())
        res["status"] = "failed"
        res["msg"] = runs_url + " api error"

    return {
        "headers": { "Access-Control-Allow-Origin": "*"},
        "statusCode": 200 if res["status"] == "success" else 502,
        "body": json.dumps(res)
    }
