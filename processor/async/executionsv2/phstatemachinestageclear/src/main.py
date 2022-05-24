import boto3


def lambda_handler(event, context):
    print(event)
    
    # 1. delete cloudformation with arn
    stackName = "-".join([event['runnerId'], "step", str(event["index"])]).replace("_", "-").replace(":", "-").replace("+", "-").replace(" ", "-")
    client = boto3.client('cloudformation')
    response = client.delete_stack(
        StackName=stackName # event['runnerId']
    )
    print(response)
    
    return {}
