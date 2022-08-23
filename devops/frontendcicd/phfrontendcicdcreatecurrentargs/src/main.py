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
                "stackName": "",
                "componentPrefix": "",
                "buildSpec": "",
                "codebuildCfn": "",
                "componentName": "",
                "branchName": "",
                "repoName": "",
                "version": "",
                "runtime": "",
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
    currentComponentMsg = event["componentArgs"][lmdIndex]
    currentComponentArgs = {
        "name": currentComponentMsg["stackName"],
        "cfn": currentComponentMsg["codebuildCfn"],
        "parameters": {
            "ComponentName": currentComponentMsg["componentName"],
            "RepoName": currentComponentMsg["repoName"],
            "BranchName": currentComponentMsg["branchName"],
            "GitCommit": currentComponentMsg["gitCommit"],
            "GitUrl": currentComponentMsg["gitUrl"],
            "ComponentPath": currentComponentMsg["componentPrefix"],
            "S3ComponentPath": currentComponentMsg["s3ComponentPath"],
            "ClientName": currentComponentMsg["clientName"],
            "ClientBucket": currentComponentMsg["ClientBucket"],
            "ClientId": currentComponentMsg["clientId"],
            "BuildSpec": currentComponentMsg["buildSpec"]
        }
    }

    return currentComponentArgs
