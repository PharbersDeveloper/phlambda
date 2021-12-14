import requests
import json
import boto3


# 运行指定dag
def lambda_handler(event, context):
    msg = event['body']
    dag_id = msg['run_id']
    project_name = msg.get('prject_name', 'max')

    # ssm get url
    client = boto3.client('ssm')
    response = client.get_parameter(
        Name='airflow_args',
        WithDecryption=False
    )
    ssm_dict = json.loads(response.get('Parameter').get('Value'))
    url = ssm_dict.get(project_name)
    print(url)

    res = {}
    headers = {
        # "Authorization": 'Basic Base64(webuser:password)',
        "Content-type": 'application/json',
    }

    # 如果存在dag_id将状态改为激活
    # update_url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id
    update_url = url + "/api/v1/dags/" + dag_id
    try:
        body = {"is_paused": False}
        result = requests.patch(url=update_url, data=json.dumps(body), headers=headers)
        if result.status_code != 200:
            res["status"] = "Failed"
            res["msg"] = dag_id + " Activation failed"

    except:
        res["status"] = "Failed"
        res["msg"] = update_url + "api error"

    # dag_id状态激活后即可开始run
    # runs_url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/dagRuns"
    runs_url = url + "/api/v1/dags/" + dag_id + "/dagRuns"
    try:
        dag_runs = requests.post(url=runs_url, headers=headers)
        if dag_runs.status_code == 200:
            res["status"] = "Success"
            run_time = str(dag_runs.json()["dag_runs"][-1]["execution_date"]).replace(':', '_')
            print(run_time)
            res["msg"] = dag_id + "_" + run_time
        else:
            res["status"] = "Failed"
            res["msg"] = dag_id + " Trigger failure"

    except:
        res["status"] = "Failed"
        res["msg"] = runs_url + " api error"

    return {
        "statusCode": 200 if res["status"] == "Success" else 502,
        "body": json.dumps(res)
    }
