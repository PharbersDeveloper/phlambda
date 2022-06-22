import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')
'''
将错误提取出来写入到notification中
args:
    event = {
        "iterator": {
            "index": 1,
            "currentStatus": running
        }
        "lambdaArgs": [
            {   
                "stackName": ""
                "functionPath": "",
                "functionPrefixPath": "",
                "buildSpec": "",
                "codebuildCfn": "",
                "functionName": "",
                "branchName": "",
                "repoName": "",
                "alias": "",
                "gitCommit": "",
                "gitUrl": ""
            }, {...}
        ]
    }
return:
    {
        "currentLmdArgs": {
            {
                "name": "functionName + codebuild"
                "cfn": "codebuildS3Path",
                "parameters": {
                    "functionPath": "",
                    "functionName": "",
                    "branchName"："",
                    "repoName": "",
                    "alias": "",
                    "gitUrl": ""
                }
            }
        }
    }

'''


def lambda_handler(event, context):
    print(event)
    lmdIndex = event["iterator"]["index"]
    currentlambdaMsg = event["lambdaArgs"][lmdIndex]
    currentLmdArgs = {
        "name": currentlambdaMsg["stackName"],
        "cfn": currentlambdaMsg["codebuildCfn"],
        "parameters": {
            "FunctionName": currentlambdaMsg["functionName"],
            "BuildSpec": currentlambdaMsg["buildSpec"],
            "FunctionPath": currentlambdaMsg["functionPath"],
            "FunctionPathPrefix": currentlambdaMsg["functionPrefixPath"],
            "GitCommit": currentlambdaMsg["gitCommit"],
            "GitUrl": currentlambdaMsg["gitUrl"],
            "BranchName": currentlambdaMsg["branchName"],
            "RepoName": currentlambdaMsg["repoName"],
            "Alias": currentlambdaMsg["alias"]
        }
    }

    return currentLmdArgs
