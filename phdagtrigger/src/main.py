import subprocess
import json


def lambda_handler(event, context):
    msg = event['body']

    run_id = msg['run_id']
    project_name = msg['project_name']
    dag_name = project_name
    job_id = msg['job_id']
    job_name = msg['job_name']

    res = {}
    ret = subprocess.run('airflow dags unpause ' + dag_name, shell=True, capture_output=True, text=True)
    if ret.returncode != 0:
        res["status"] = 'Failed'
        res["msg"] = dag_name + " Activation failed"
        # return JsonResponse(res)

        # 运行指定dag
        ret = subprocess.run('airflow dags trigger ' + dag_name, shell=True, capture_output=True, text=True)
        if ret.returncode == 0:
            res["status"] = 'Success'
            res["msg"] = dag_name + " Trigger a success"
        else:
            res["status"] = "Failed"
            res["msg"] = dag_name + " Trigger failure"

    else:
        res["status"] = "Failed"
        res["msg"] = "Not GET request"

    return {
        "statusCode": 200 if res["status"] == "Success" else 502,
        "body": json.dumps(res)
    }
