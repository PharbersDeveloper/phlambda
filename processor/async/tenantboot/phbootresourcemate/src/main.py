import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

'''
这个从resource表中读取需要创建的资源的matedata的描述
也就是所从emr中读取emr的配

args = {
    "tenantId.$": "$.common.tenantId",
    "traceId.$": "$.common.traceId",
    "projectId.$": "$.common.projectId",
    "owner.$": "$.common.owner",
    "showName.$": "$.common.showName",
    "resources.$": "$.resources"
}

return = {
    "metadata": {
        "engine": [
            {   
                "type": "emr",
                "version": "emr-6.2.0",
                "label": [
                    {
                        "spark": "3.0.2",
                        "hadoop": "3.2.0"
                    }
                ]
                "cfn": "",
                "stackName": "",
                "parameters": {
                    "RootVolumeSize": 10,
                    "MasterInstanceType": "m5.2xlarge",
                    "MasterStorage": 64,
                    "CoreInstanceType": "m5.2xlarge",
                    "CoreStorage": 32,
                    "InitialCoreSize": 1,
                    "MaxCoreSize": 2,
                    "TaskInstanceType": "m5.2xlarge",
                    "TaskStorage": 32,
                    "TaskNodeOutThreshold": 10,
                    "InitialTaskSize": 2,
                    "MaxTaskSize": 10
                }
            }
        ],
        "olap": [
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


def get_resource_items_by_tenantId(tenantId):
    ds_table = dynamodb.Table('resource')
    res = ds_table.query(
        KeyConditionExpression=Key("tenantId").eq(tenantId)
    )

    return res["Items"]


def lambda_handler(event, context):
    print(event)
    # 获取有关tenantId的所有信息
    tenant_all_items = get_resource_items_by_tenantId(event["tenantId"])

    # 进行filter 查找
    metadata = {}

    # tenant_items = [item["ownership"] == "shared" for item in tenant_all_items]
    tenant_items = list(filter(lambda x: x["ownership"] == "shared", tenant_all_items))
    print(tenant_items)
    # TODO: resources 里面的值与tenantItems 里面role值求交集，只有交集才能创建 @hbzhao

    for tenant_item in tenant_items:
        tmp = {}
        tmp = json.loads(tenant_item["properties"])
        for item in tmp:
            item["stackName"] = "-".join([tenant_item["role"], item["type"], event["tenantId"]])
        
        metadata[tenant_item["role"]] = {
            "counts": len(tmp),
            "steps": tmp
        }

    print(metadata)
    return metadata
