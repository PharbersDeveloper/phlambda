import json
import boto3
from boto3.dynamodb.conditions import Key

'''
这个函数是对所有的personal resouce boot 的 clean up
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "personalResBoots",
        "desc": "reboot project",
        "comments": "something need to say",
        "message": "something need to say",
        "required": true
    },
    "resourceId": "",
    "stackName:": "",
    "notification": {
        "required": true
    }
}
'''

class CleanUp:
    cloudformation = boto3.client('cloudformation')
    ssm = boto3.client('ssm')
    dynamodb = boto3.resource('dynamodb')

    def query_resource(self, tenantId):
        table = self.dynamodb.Table("resource")
        response = table.query(
            KeyConditionExpression=Key('tenantId').eq(tenantId),
        )
        return response.get("Items")

    def list_cloudformation_ssm_name(self, resource, resourceId):
        stackNameList = []
        ssmNameList = []
        properties = json.loads(resource["properties"])
        for prop in properties:
            stackName = "-".join([resource["role"], prop["type"], resourceId, resource["ownership"],
                                  resource["owner"]]).replace("_", "-").replace(":", "-").replace("+", "-")

            ssmName = '-'.join([prop['type'], resource['owner'], resourceId])
            stackNameList.append(stackName)
            ssmNameList.append(ssmName)
        return stackNameList, ssmNameList

    def del_stack(self, stackname):
        response = self.cloudformation.delete_stack(
            StackName=stackname,
        )

    def del_ssm(self, ssm_name):
        response = self.ssm.delete_parameter(
            Name=ssm_name
        )

    def run(self, tenantId, resourceId, **kwargs):
        cloudformation_names, ssm_names = self.list_cloudformation_ssm_name(tenantId, resourceId)
        for stack_name in cloudformation_names:
            self.del_stack(stack_name)
        for ssm_name in ssm_names:
            ssm_name = ssm_name.replace("=", "-")
            self.del_ssm(ssm_name)


# 1. stackName 存在就删除
def lambda_handler(event, context):
    print(event)
    errors = event.get("error")
    try:
        CleanUp().run(**event)
    except:
        pass

    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
        }
    }
