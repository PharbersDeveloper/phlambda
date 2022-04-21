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

        stateMachineName = event['runnerId'].replace("_", "-").replace(":", "-").replace("+", "-")
        stateMachineArn = "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:" + stateMachineName
        sfn_client = boto3.client('stepfunctions')
        events = sfn_client.list_executions(
            stateMachineArn=stateMachineArn
        )
        executionArn = events["executions"][0]["executionArn"]
        events = sfn_client.stop_execution(executionArn=executionArn)

        result_message = {
            "status": "ok",
            "data": {
                "message": "stop dag success"
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
