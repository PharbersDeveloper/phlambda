import json
import boto3
from boto3.dynamodb.conditions import Key

'''
同步错误，清理 cloudformation 以及 SSM 资源

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
    ],
    "error": {
        "EMRError": {
            "Error": "",
            "Cause": ""
        },
        "EC2Error": {
            "Error": "",
            "Cause": ""
        }
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

    def get_stack_name(self, tenantId):
        resource_item = self.query_resource(tenantId)
        item_list = [item for item in resource_item if item.get("ownership") == "shared"]

        res_list = []
        for item in item_list:
            res_list += [
                f'{item.get("role")}-{property.get("type")}-{tenantId.replace("_", "-").replace(":", "-").replace("+", "-")}'
                for property in json.loads(item.get("properties"))]

        return res_list

    def del_stack(self, stackname):
        response = self.cloudformation.delete_stack(
            StackName=stackname,
        )

    def del_ssm(self, ssm_name):
        response = self.ssm.delete_parameter(
            Name=ssm_name
        )

    def run(self, tenantId, **kwargs):
        for stack_name in self.get_stack_name(tenantId):
            self.del_stack(stack_name)
        self.del_ssm(tenantId)


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
