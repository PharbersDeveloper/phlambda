import boto3


def lambda_handler(event, context):
    # cicd 1317
    print(event)    
    
    # 1. delete cloudformation with arn
    stackName = event['runnerId'].replace("_", "-").replace(":", "-").replace("+", "-")
    client = boto3.client('cloudformation')
    response = client.delete_stack(
        StackName=stackName # event['runnerId']
    )
    print(response)
    
    return {}
