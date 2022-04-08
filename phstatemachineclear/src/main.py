import boto3


def lambda_handler(event, context):
    print(event)    
    
    # 1. delete cloudformation with arn
    client = boto3.client('cloudformation')
    response = client.delete_stack(
        StackName=event['runnerId']
    )
    print(response)
    
    return {}
