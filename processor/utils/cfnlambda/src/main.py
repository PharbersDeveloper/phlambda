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
        "action": "creation | deletion",
        "name": "",
        "cfn": "",
        "parameters" [
            
        ],
        "dependencies.$": "$.currentStep.dependencies",
        "result.$": "$.engine"
    }

return:
    {
        
    }
'''


def lambda_handler(event, context):
    print(event)
    # TODO: dependencies

    stackName = event["name"].replace("_", "-").replace(":", "-").replace("+", "-")

    if event["action"] == "creation":
        cfnPath = event["cfn"]
        parameters = []
        for item in event["parameters"].keys():
            tmp = {}
            tmp["ParameterKey"] = item
            tmp["ParameterValue"] = event["parameters"][item]
            parameters.append(tmp)
        
        response = client.create_stack(
            StackName=stackName,
            TemplateURL=cfnPath,
            Parameters=parameters)
        print(response)

    elif event["action"] == "deletion":
        response = client.delete_stack(
            StackName=stackName
        )

    return True
