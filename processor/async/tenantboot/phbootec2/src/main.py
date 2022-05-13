import json
import boto3

'''
这个从resource表中读取需要创建的资源的matedata的描述
也就是所从project中读取project的配置
现在是ec2 从ec2中读取他的配置

这个是为了支持现有的固定流程，以后会被取缔，
可以直接用@赵浩博的project启动版本

args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "resources": [
        "emr", "ec2"
    ]
}

return = {
    "matedata" {
        "ec2": {
    
        }
    }
}
'''


def create_cloudformation(stackName, cfn_path, parameters):
    cfn_client = boto3.client("cloudformation")
    cfn_client.create_stack(
        StackName=stackName,
        TemplateURL=cfn_path,
        Parameters=parameters
    )


def lambda_handler(event, context):

    # 获取参数 创建cloudformation


    return True
