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
    "resourceId.$": "$.resourceId"
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


def get_resource_items_by_tenantId(tenantId, id):
    ds_table = dynamodb.Table('resource')
    res = ds_table.query(
        KeyConditionExpression=Key("tenantId").eq(tenantId) & Key("id").eq(id)
    )

    return res["Items"]


def lambda_handler(event, context):
    print(event)
    # 获取有关tenantId的所有信息
    tenant_all_items = get_resource_items_by_tenantId(event["tenantId"], str(event["resourceId"]).replace("=", "-"))

    metadata = {}

    for tenant_item in tenant_all_items:
        tmp = {}
        tmp = json.loads(tenant_item["properties"])
        for item in tmp:
            item["stackName"] = "-".join([tenant_item["role"], item["type"], event["tenantId"], tenant_item["ownership"], tenant_item["owner"]])
        
        metadata[tenant_item["role"]] = {
            "counts": len(tmp),
            "steps": tmp
        }

    print(metadata)
    return metadata
