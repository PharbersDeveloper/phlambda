import boto3
from util.AWS.PhAWS import PhAWS

class ELB(PhAWS):

    def __init__(self, **kwargs):

        self.cfn_client = boto3.client("cloudformation")

    def create_ec2(self):

        cfn_client.create_stack(
            StackName= self.target_name + "project",
            TemplateURL='https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cloudformation/glue/crawler/phcrawler.yaml',
            Parameters=[
                {
                    'ParameterKey': 'DatabaseName',
                    'ParameterValue': database,
                },
                {
                    'ParameterKey': 'CrawlerName',
                    'ParameterValue': crawlerName,
                },
                {
                    'ParameterKey': 'S3TargetPath',
                    'ParameterValue': S3TargetPath,
                }
            ]
        )