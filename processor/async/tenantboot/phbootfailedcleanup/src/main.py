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
    cloudformation = boto3.client('cloudformation', region_name="cn-northwest-1",
                                  aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                                  aws_secret_access_key="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")

    def del_stack(self, stackname):
        response = self.cloudformation.delete_stack(
            StackName=stackname,
        )

    def run(self, traceId, **kwargs):
        self.del_stack(traceId)



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

