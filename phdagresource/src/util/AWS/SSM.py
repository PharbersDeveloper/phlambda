import boto3
from util.AWS.PhAWS import PhAWS

class CFN(PhAWS):

    def __init__(self, **kwargs):

        self.ssm_client = boto3.client('ssm')

    def put_ssm_parameter(self):

        response = self.ssm_client.put_parameter(
            Name='string',
            Description='string',
            Value='string',
            Type='String'|'StringList'|'SecureString',
            KeyId='string',
            Overwrite=True|False,
            AllowedPattern='string',
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            Tier='Standard'|'Advanced'|'Intelligent-Tiering',
            Policies='string',
            DataType='string'
        )