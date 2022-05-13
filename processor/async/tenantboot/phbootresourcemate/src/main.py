import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

'''
这个从resource表中读取需要创建的资源的matedata的描述
也就是所从emr中读取emr的配

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
    "metadata": {
        "emr": {
            "Common": {
                "RootVolumeSize": 10,
                "ReleaseLabel": "emr-6.2.0"
            },
            "Master": {
                "MasterInstanceType": "m5.2xlarge",
                "MasterStorage": 64
            },
            "Core": {
                "CoreInstanceType": "m5.2xlarge"
                "CoreStorage": 32,
                "InitialCoreSize": 1,
                "MaxCoreSize": 2
            },
            "Task": {
                "TaskInstanceType": "m5.2xlarge",
                "TaskStroage": 32,
                "TaskNodeOutThreshold": 10,
                "InitialTaskSize": 2,
                "MaxTaskSize": 10
            }
        }
    }
}
'''


def get_resource_items_by_tenantId(tenantId, role):
    ds_table = dynamodb.Table('resource')
    res = ds_table.query(
        IndexName='resource-tenantId-role-index',
        KeyConditionExpression=Key("tenantId").eq(tenantId)
                               & Key("role").eq(role)
    )

    return res["Items"]


def lambda_handler(event, context):

    # 从dynamodb 根据tenantId获取有关engine的信息

    # 从dynamodb 根据tenantId获取有关olap的信息
    # 从dynamodb 根据tenantId获取有关codeeditor的信息

    return True
