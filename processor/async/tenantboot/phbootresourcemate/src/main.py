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
        "engine", "olap"
    ]
}

return = {
    "metadata": {
        "engines": [
            {   
                "type": "ec2",
                "cfn": "",
                "parameters": {
                    "RootVolumeSize": 10,
                    "ReleaseLabel": "emr-6.2.0",
                    "MasterInstanceType": "m5.2xlarge",
                    "MasterStorage": 64,
                    "CoreInstanceType": "m5.2xlarge"
                    "CoreStorage": 32,
                    "InitialCoreSize": 1,
                    "MaxCoreSize": 2，
                    "TaskInstanceType": "m5.2xlarge",
                    "TaskStorage": 32,
                    "TaskNodeOutThreshold": 10,
                    "InitialTaskSize": 2,
                    "MaxTaskSize": 10
                }
            }
        ],
        "olaps": [
            {
                "type": "ec2",
                "cfn": "",
                "parameters": {
                    "RootVolumeSize": 10,
                    "ReleaseLabel": "emr-6.2.0"
                }
            }
        ]
            
    }
}
'''

cfn_path = {
    "clickhouse": "",
    "emr": ""
}


def get_resource_items_by_tenantId(tenantId):
    ds_table = dynamodb.Table('resource')
    res = ds_table.query(
        KeyConditionExpression=Key("tenantId").eq(tenantId)
    )

    return res["Items"]


def create_engine_args(tenant_item):

    args = tenant_item["properties"]
    args["cfn"] = cfn_path[tenant_item["ctype"]]

    return args


def create_olap_args(tenant_item):

    args = tenant_item["properties"]
    args["cfn"] = cfn_path[tenant_item["ctype"]]

    return args


def lambda_handler(event, context):

    # 获取有关tenantId的所有信息
    tenant_all_items = get_resource_items_by_tenantId(event["tenantId"])
    # 进行filter 查找
    metadata = {}
    engine_metadata_list = []
    olap_metadata_list = []

    tenant_items = [item["ownership"] == "shared" for item in tenant_all_items]
    for tenant_item in tenant_items:
        # 从dynamodb 根据tenantId获取有关engine的信息
        if tenant_item["role"] == "engine":
            engine_metadata = create_engine_args(tenant_item)
            engine_metadata_list.append(engine_metadata)
        # 从dynamodb 根据tenantId获取有关olap的信息
        if tenant_item["role"] == "olap":
            olap_metadata = create_olap_args(tenant_item)
            olap_metadata_list.append(olap_metadata)

    return metadata
