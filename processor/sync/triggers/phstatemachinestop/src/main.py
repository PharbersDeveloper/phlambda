import boto3
import json


def lambda_handler(event, context):
    result_code = 200
    result_message = {}
    try:
        event = event['body']
        if type(event) == str:
            event = json.loads(event)
        print(event)

        run_id = event['runnerId']
        tenant = "pharbers"
        dag_name = "_".join(run_id.split("_")[:-1])
        s3_bucket = "ph-platform"
        s3_prefix = f"2020-11-11/jobs/statemachine/{tenant}/{dag_name}/{run_id}/"
        step_name = run_id.replace("_", "-").replace(":", "-").replace("+", "-")

        s3 = boto3.client("s3", region_name="cn-northwest-1")
        response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_prefix)

        file_number = response["KeyCount"]

        if file_number > 0:
            stateMachineName = f"{step_name}-step-{file_number}"
            stateMachineArn = "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:" + stateMachineName
            sfn_client = boto3.client('stepfunctions')
            events = sfn_client.list_executions(
                stateMachineArn=stateMachineArn
            )
            executionArn = events["executions"][0]["executionArn"]
            sfn_client.stop_execution(executionArn=executionArn)

            result_message = {
                "status": "ok",
                "data": {
                    "message": "stop dag success"
                }
            }
        else:
            result_message = {
                "status": "ok",
                "data": {
                    "message": "dag no running"
                }
            }

    except Exception as e:
        result_message = {
            "status": "error",
            "data": {
                "message": "stop dag failure: " + str(e)
            }
        }

    if result_message["status"] == "error":
        result_code = 503

    return {
        "statusCode": result_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        },
        "body": json.dumps(result_message)
    }
