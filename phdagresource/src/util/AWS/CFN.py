import boto3
from util.AWS.PhAWS import PhAWS

class CFN(PhAWS):

    def __init__(self, **kwargs):

        self.cfn_client = boto3.client("cloudformation")

    def create_project(self, project_id, parameters):

        self.cfn_client.create_stack(
            StackName="project-" + project_id,
            TemplateURL='https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/automation/bastionhost-resource-dev.yaml',
            Parameters=parameters
        )

    def delete_project(self, stack_name):

        self.cfn_client.delete_stack(
            StackName="project-" + stack_name
        )