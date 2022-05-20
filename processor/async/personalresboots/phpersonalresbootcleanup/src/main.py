import json
import boto3

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


# 1. stackName 存在就删除
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
