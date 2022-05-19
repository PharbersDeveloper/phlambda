import json
import boto3
from boto3.dynamodb.conditions import Attr, Key


'''
通过参数，删除所有的steps
args = {
    "traceId.$": "$.common.traceId",
    "projectId.$": "$.common.projectId",
    "owner.$": "$.common.owner",
    "showName.$": "$.common.showName",
    "resources.$": "$.resources"
}
'''


dynamodb = boto3.resource("dynamodb")
client = boto3.client('cloudformation')


def lambda_handler(event, context):


    # 1. 从dynamodb中拿出所有的 tenantId 下的所有角色
    table = dynamodb.Table("resource")
    resources = table.query(
        KeyConditionExpression=Key("tenantId").eq(event["tenantId"]),
        FilterExpression=Attr("ownership").ne("static")
    )["Items"]
    
    print(resources)

    stackNames = []
    # 2. 找到所有的resouce，并生成需要修改的 stack name
    for tenant_item in resources:
        tmp = json.loads(tenant_item["properties"])
        for item in tmp:
            stackNames.append("-".join([tenant_item["role"], item["type"], event["tenantId"]]))


    stackNames = list(map(lambda x: x.replace("_", "-").replace(":", "-").replace("+", "-"), stackNames))

    # 3. 对每一个存在的 stack name 做删除 stack 的操作
    print(stackNames)
    for sn in stackNames:
        try:
            client.delete_stack(
                StackName=sn
            )
        except Exception:
            pass

    return {
        "stackNames": stackNames,
        "wait": True
    }
