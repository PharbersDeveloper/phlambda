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


def check_stack(stackName):
    result = False
    try:
        response = cfn_client.describe_stacks(
            StackName=stackName
        )
        status = [
            'CREATE_IN_PROGRESS','CREATE_FAILED','CREATE_COMPLETE','ROLLBACK_IN_PROGRESS','ROLLBACK_FAILED','ROLLBACK_COMPLETE','DELETE_IN_PROGRESS','DELETE_FAILED','DELETE_COMPLETE','UPDATE_IN_PROGRESS','UPDATE_COMPLETE_CLEANUP_IN_PROGRESS','UPDATE_COMPLETE','UPDATE_FAILED','UPDATE_ROLLBACK_IN_PROGRESS','UPDATE_ROLLBACK_FAILED','UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS','UPDATE_ROLLBACK_COMPLETE','REVIEW_IN_PROGRESS','IMPORT_IN_PROGRESS','IMPORT_COMPLETE','IMPORT_ROLLBACK_IN_PROGRESS','IMPORT_ROLLBACK_FAILED','IMPORT_ROLLBACK_COMPLETE',
        ]
        if len(response['Stacks']) > 0 and response['Stacks'][0]['StackStatus'] in status:
            result = True
    except botocore.exceptions.ClientError as e:
        print("stackName不存在")
    return result


def create_stack(stackName, cfnPath, stepFunctionArgs):
    parameters = []
    for item in stepFunctionArgs.keys():
        tmp = {}
        tmp["ParameterKey"] = item
        tmp["ParameterValue"] = stepFunctionArgs[item]
        parameters.append(tmp)
    response = cfn_client.create_stack(
        StackName=stackName,
        TemplateURL=cfnPath,
        Parameters=parameters,
        Capabilities=['CAPABILITY_AUTO_EXPAND']
    )


def create_stack_change_set(stackName, cfnPath, stepFunctionArgs, changeSetName):
    parameters = []
    for item in stepFunctionArgs.keys():
        tmp = {}
        tmp["ParameterKey"] = item
        tmp["ParameterValue"] = stepFunctionArgs[item]
        parameters.append(tmp)
    response = cfn_client.create_change_set(
        StackName=stackName,
        TemplateURL=cfnPath,
        Parameters=parameters,
        ChangeSetName=changeSetName,
        ChangeSetType="UPDATE",
        Capabilities=['CAPABILITY_AUTO_EXPAND']
    )
    return response["Id"]



def lambda_handler(event, context):
    print(event)
    changeSetName = None
    stackName = event["stackName"]
    manageUrl = event["manageUrl"]
    if check_stack(stackName):
        changeSetName = stackName + "-" + event["version"]
        create_stack_change_set(stackName, manageUrl, event["stepFunctionArgs"], changeSetName)
    else:
        create_stack(stackName, manageUrl, event["stepFunctionArgs"])
    return {
        "stackName": stackName,
        "changeSetName": changeSetName
    }