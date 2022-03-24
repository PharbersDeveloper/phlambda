import boto3
from util.AWS.PhAWS import PhAWS

class CFN(PhAWS):

    def __init__(self, **kwargs):

        self.cfn_client = boto3.client("cloudformation")

    def create_project(self, target_name, target_ip, project_id):

        self.cfn_client.create_stack(
            StackName=target_name + "-project",
            TemplateURL='https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/automation/bastionhost-cfn-tmp.yaml',
            Parameters=[
                {
                    'ParameterKey': 'ProjectName',
                    'ParameterValue': target_name,
                },
                {
                    'ParameterKey': 'PrivateIpAddress',
                    'ParameterValue': target_ip,
                },
                {
                    'ParameterKey': 'ProjectId',
                    'ParameterValue': project_id,
                }
            ]
        )

    def delete_project(self, stack_name):

        self.cfn_client.delete_stack(
            StackName=stack_name + "-project"
        )