import json
import boto3

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
    cloudformation = boto3.client('cloudformation', region_name="cn-northwest-1")
    ssm = boto3.client('ssm', region_name="cn-northwest-1")

    def del_stack(self, stackname):
        response = self.cloudformation.delete_stack(
            StackName=stackname,
        )

    def del_ssm(self, ssm_name):
        response = self.ssm.delete_parameter(
            Name=ssm_name
        )

    def run(self, traceId, **kwargs):
        self.del_stack(traceId)
        self.del_ssm(traceId)



def lambda_handler(event, context):
    common = event.get("common")
    errors = event.get("errors")
    CleanUp().run(**common)

    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
        }
    }

