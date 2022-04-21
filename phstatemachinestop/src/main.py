import boto3


def lambda_handler(event, context):
    print(event)    
    
    # 1. delete cloudformation with arn
    stateMachineName = event['runnerId'].replace("_", "-").replace(":", "-").replace("+", "-")
    stateMachineArn = "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:" + stateMachineName
    sfn_client = boto3.client('stepfunctions')
    events = sfn_client.list_executions(
        stateMachineArn=stateMachineArn
    )
    executionArn = events["executions"][0]["executionArn"]
    events = sfn_client.stop_execution(executionArn=executionArn)

    print(executionArn)

    return {}
