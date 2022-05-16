import os
import json
import boto3
import traceback
import datetime

client = boto3.client('cloudformation')

'''
# cloud formation stack 创建与删除

args:
    event = {
        "result.$": "$.engine",
        "resultPath": "engine",
        "resultType.$": "$.currentStep.type",
        "name.$": "$.currentStep.stackName"
    }

return:
    {
        
    }
'''


def lambda_handler(event, context):
    print(event)

    stackName = event["name"].replace("_", "-").replace(":", "-").replace("+", "-")

    response = client.describe_stacks(
        StackName=stackName #  event['runnerId']
    )
    print(response)

    result = event["result"]
    if len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] == "CREATE_COMPLETE":
        stackOutputs = response['Stacks'][0]['Outputs']

        for item in stackOutputs:
            result[item["OutputKey"]] = item["OutputValue"]

    else:
        raise Exception("unknow error")

    return result
