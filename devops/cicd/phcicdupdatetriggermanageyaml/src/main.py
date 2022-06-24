import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')
'''
将错误提取出来写入到notification中
args:
    event = {
                "version": "V001",
                "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
                "publisher": "赵浩博",
                "alias": "V001",
                "runtime": "dev",
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
                },
                "apiGateWayArgs": {
                    "method": ["POST"],
                    "PathPart": "phsampletrigger",
                    "LmdName": "lmd-phsampletrigger-dev",
                    "RestApiId": "",
                    "AuthorizerId": "",
                    "ParentId": ""
                }
            },
return:
    {
        "manageUrl": manageUrl,
        "stackName": stackName，
        "stackParameters": stackParameters 
    }
}
'''
manageTemplateS3Key = "ph-platform"
manageTemplateS3Path = "2020-11-11/cicd/template/manageTemplate.yaml"
sfnTemplateS3Key = "ph-platform"
sfnTemplateS3Path = "2020-11-11/cicd/template/sfnTemplate.yaml"
resourcePathPrefix = "2020-11-11/cicd/"
manageUrlPrefix = "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cicd/"
mangeLocalPath = "/tmp/manage.yaml"
sfnLocalPath = "/tmp/sfnTemplate.yaml"


def lambda_handler(event, context):

    # 1 下载ApiResource文件、
    #   POST, GET, OPTIONS, DELETE, PATCH 每个method使用一种模板
    # 2 下载manage template文件
    # 3 将 api 相关信息写入到 manage中
    # 4 下载function的package.yaml文件 resourcePathPrefix + functionPath + "/package/package.yaml"
    # 5 将 function package文件内容写入 manage中
    # 6 上传manage文件 manageUrlPrefix + event["trigger"]["prefix"] + "/manage.yaml"

    return 1
