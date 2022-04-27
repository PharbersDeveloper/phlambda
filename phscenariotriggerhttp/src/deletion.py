import boto3

def scenarioDLProcessor(tenantId, targetArn, projectId, scenarioId, triggerId):
	result = {}

    stackName = "-".join(["scenario", projectId, scenarioId, triggerId])    
    client = boto3.client('cloudformation')
    response = client.delete_stack(
        StackName=stackName # event['runnerId']
    )
    print(response)
    result['status'] = 'ok'
    result['message'] = 'delete resource success'

    return result
    