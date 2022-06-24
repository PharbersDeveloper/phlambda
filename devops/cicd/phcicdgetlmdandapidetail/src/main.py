import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')
'''
处理lmd和api相关信息
args:
    event = {
        "version": "V001",
        "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
        "publisher": "赵浩博",
        "alias": "V001",
        "runtime": "dev"
        "trigger": {
            "repo": "phlambda",
            "branch": "feature/PBDP-3043-async-cicd-state-machine",
            "prefix": "processor/sync/triggers/phsampletrigger",
            "lmdName": "lmd-phsampletrigger-dev",
            "sm": "processor/async/sample/sm.json",
            "entry": {
                "type": "Api GateWay",
                "resource": "phsampletrigger"
                "method": ["POST"]
            },
            "required": true
        }
return:
    {   
        "lambdaArgs": 
            "name": "phsampletriggercodebuild",
            "cfn": "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/template/phlambda-codebuild.yaml",
            "parameters": {
              "FunctionName": "phsampletrigger",
              "BuildSpec": "lmdAndApiBuildspec",
              "FunctionPath": "processor/sync/triggers/phsampletrigger",
              "FunctionPathPrefix": "processor/sync/triggers",
              "GitCommit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
              "GitUrl": "http://hbzhao:123456@192.168.53.179:7990/scm/lgc/phlambda.git",
              "BranchName": "feature/PBDP-3043-async-cicd-state-machine",
              "RepoName": "phlambda",
              "Version": "V001"
            },
        "apiGateWayArgs": {
            "method": ["POST"],
            "PathPart": "phsampletrigger",
            "LmdName": "lmd-phsampletrigger-dev",
            "RestApiId": "",
            "AuthorizerId": "",
            "ParentId": ""
        }
    }
'''

def lambda_handler(event, context):
    print(event)
    # 1 处理lmd相关信息 返回lambdaArgs 参数用于运行codebuild
    # 2 处理apiGateway相关信息 返回apiGateWayArgs
    # RestApiId AuthorizerId ParentId 根据runtime进行获取

    return 1
