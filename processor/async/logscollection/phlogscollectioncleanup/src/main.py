import json
import boto3

'''
理论上只有超时才会走到这里
args = {
    "common": {
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "owner": "alfred",
        "showName": "alfred"
    },
    "clusterId": "",
    "stepId": ""
}
'''

class CleanUp:
    cloudformation = boto3.client('cloudformation', region_name="cn-northwest-1")
    ssm = boto3.client('ssm', region_name="cn-northwest-1")

    def del_stack(self, stackname):
        response = self.cloudformation.delete_stack(
            StackName=stackname,
        )

    def run(self, traceId, **kwargs):
        self.del_stack(traceId)


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
