import json
import datetime

def lambda_handler(event, context):
    print(event)
    dag_name = event['dag_name']
    run_id = dag_name + "_" + (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d_%H-%M-%S")

    return {
        "run_id" : run_id,
    }
