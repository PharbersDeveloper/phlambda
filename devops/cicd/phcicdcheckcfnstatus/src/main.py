import boto3
import botocore

cfn_client = boto3.client('cloudformation')
'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "common": {
            "version": "version",
            "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
            "publisher": "赵浩博",
            "alias": "hbzhao-resource-change-position-owner",
            "runtime": "dev/v2/prod"
        },
        "processor": {
            "repo": "phlambda",
            "branch": "",
            "prefix": "processor/async/createscriptrefile",
            "stateMachineName": "createscriptrefile",
            "sm": "processor/async/createscriptrefile/sm.json",
            "functions": [
                {   
                    "name": "phresourcepycodegen"
                },
                {
                    "name": "phresourcercodegen"
                }
            ]
            "required": true
        },
        "trigger": {
            "repo": "phlambda",
            "branch": "",
            "prefix": "processor/sync/utils/phemail",
            "stateMachineName": "createscriptrefile",
            "name": "phemail"
            "entry": {
                "type": "ApiGateway",
                "resource": "",
                "method": ""
            }
            "required": true      
        }
    }
'''


def check_stack_change_set(stackName):
    result = False
    sucessStatus = ["CREATE_COMPLETE", "UPDATE_COMPLETE"]
    response = cfn_client.describe_stacks(
        StackName=stackName
    )
    if response['Status'] in sucessStatus and len(response['Stacks']) > 0:
        result = True
    elif len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] == "ROLLBACK_COMPLETE":
        raise Exception('create ' + stackName + ' failed')
    return result


def lambda_handler(event, context):
    print(event)
    changeSetStatus = check_stack_change_set(event["stackName"])

    return changeSetStatus