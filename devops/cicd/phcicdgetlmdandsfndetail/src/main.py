import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')
'''
处理lmd和sfn的相关信息
args:
    event = {
        "version": "20220622",
        "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
        "publisher": "赵浩博",
        "alias": "Current",
        "runtime": "dev"
        "processor": {
            "repo": "phlambda",
            "branch": "feature/PBDP-3043-async-cicd-state-machine",
            "prefix": "processor/async/sample",
            "stateMachineName": "sample",
            "sm": "processor/async/sample/sm.json",
            "functions": [
                {   
                    "name": "phsampleclear"
                },
                {
                    "name": "phsampledag"
                },
                {
                    "name": "phsamplefailedhook"
                },
                {
                    "name": "phsamplegen"
                },
                {
                    "name": "phsamplehook"
                }
            ]
            "required": true
        }
return:
    {   
        "lmdCounts": 1,
        "iterator": {
            "index"：0,
            "currentStatus": running
        },
        "lambda": [
            {   
                "name": "functionName"
                "functionPath": "",
                "cfn": "codebuildS3Path",
                "functionName": "",
                "branchName"："",
                "repoName": "",
                "alias": "",
                "gitUrl": ""
            }, {...}
        ],
        "sfn": {
            "stateMachineName": "functionName + codebuild",
            "submitOwner": "",
            "s3Bucket": "",
            "s3TemplateKey": ""
        }
    }

'''
codebuild_cfn_path = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/template/phlambda-codebuild.yaml"
git_url = "http://hbzhao:123456@192.168.53.179:7990/scm/lgc/phlambda.git"


def create_lambda_args(event):
    lambda_args = []
    processor = event["processor"]
    for func in processor["functions"]:
        func_args = {
            "stackName": func["name"] + "codebuild",
            "functionPath": processor["prefix"] + "/" + func["name"],
            "codebuildCfn": codebuild_cfn_path,
            "functionName": func["name"],
            "branchName": processor["branch"],
            "repoName": processor["repo"],
            "alias": event["alias"],
            "gitUrl": git_url
        }
        lambda_args.append(func_args)

    return lambda_args


def create_step_function_args(event):

    stepfuntionArgs = {
        "stateMachineName": event["processor"]["stateMachineName"],
        "submitOwner": event["publisher"],
        "s3Bucket": "phplatform",
        "s3TemplateKey": "2020-11-11/cicd/" + event["processor"]["prefix"] + "/sm.json"
    }

    return stepfuntionArgs


def lambda_handler(event, context):
    print(event)
    # 计算需要发布lmd的数量
    lmdCounts = len(event["processor"]["functions"])
    # 设置iterator
    iterator = {
        "index": 0,
        "currentStatus": "running"
    }
    # 处理lambda相关信息
    lambdaArgs = create_lambda_args(event)
    # 处理step function相关信息
    stepfuntionArgs = create_step_function_args(event)

    return 1
