import boto3
from boto3.dynamodb.conditions import Key

cfn_client = boto3.client('cloudformation')
'''

args:
    event = {
        "common": {
            "version": "version",
            "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
            "publisher": "赵浩博",
            "alias": "hbzhao-resource-change-position-owner",
            "runtime": "dev/v2/prod"
        }
    }
'''


def judge_stack_exist(stackName):
    stack_exist = False
    try:
        response = cfn_client.describe_stacks(
            StackName=stackName
        )
        stack_exist = True
        print(response)
    except Exception as e:
        print(e)
    return stack_exist


def delete_stack(stackName):
    response = cfn_client.delete_stack(
        StackName=stackName
    )


def lambda_handler(event, context):
    print(event)
    # 删除codebuild
    for component in event["frontend"]["components"]:
        stackName = component["prefix"].split("/")[-1] + "codebuild"
        if judge_stack_exist(stackName):
            delete_stack(stackName)
    return 1
