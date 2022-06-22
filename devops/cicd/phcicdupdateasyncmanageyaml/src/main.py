import json
import yaml
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
s3_client = boto3.client('s3')
'''
将错误提取出来写入到notification中
args:
    event = {   
                "version": "20220622",
                "commit": "9f2b50e4bc89dd903f85ef1215f0b31079537450",
                "publisher": "赵浩博",
                "alias": "Current",
                "runtime": "dev",
                "lambdaArgs": [
                    {   
                        "stackName": "functionName"
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
                ],
                "stepFunctionArgs": {
                    "stateMachineName": "functionName + codebuild",
                    "submitOwner": "",
                    "s3Bucket": "",
                    "s3TemplateKey": ""
                }
            },
return:
    {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
    }
}
'''


def download_s3_file(package_s3_key, package_s3_path, local_path):
    with open(local_path, 'wb') as data:
        s3_client.download_fileobj(package_s3_key, package_s3_path, data)


def read_yaml_file(file_path):
    with open(file_path, encoding='utf-8') as file:
        result = yaml.load(file.read(), Loader=yaml.FullLoader)
    return result


def lambda_handler(event, context):
    print(event)
    # 获取每个function package.yaml的内容
    # 获取functionPath拼接出s3路径
    for lambdaArg in event["lambdaArgs"]:
        functionPath = lambdaArg["functionPath"]
        package_s3_key = "ph-platform"
        package_s3_path = "2020-11-11/cicd/" + functionPath + "/package/package.yaml"
        package_local_path = "/tmp/" + lambdaArg["functionName"] + "/package.yaml"
        # 从s3下载yaml文件
        download_s3_file(package_s3_key, package_s3_path, package_local_path)
        # 写入到manage模板文件
    # 获取创建step function的参数
    # 读取step function模板文件

    return 1
