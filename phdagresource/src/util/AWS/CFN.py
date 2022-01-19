import boto3
from util.AWS.PhAWS import PhAWS

class CFN(PhAWS):

    def __init__(self, **kwargs):

        self.cfn_client = boto3.client("cloudformation")

    def create_project(self):

        self.cfn_client.create_stack(
            StackName= self.target_name + "project",
            TemplateURL='https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/automation/bastionhost-cfn.yaml',
            Parameters=[
                {
                    'ParameterKey': 'ProjectName',
                    'ParameterValue': self.target_name,
                },
            ]
        )