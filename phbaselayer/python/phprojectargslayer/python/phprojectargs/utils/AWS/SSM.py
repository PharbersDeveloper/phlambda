import boto3
import json
from phprojectargs.utils.AWS.PhAWS import PhAWS


class SSM(PhAWS):

    def __init__(self, **kwargs):

        self.ssm_client = boto3.client('ssm')

    def put_ssm_parameter(self, parameter_name, parameter_value):

        response = self.ssm_client.put_parameter(
            Name=parameter_name,
            # Description='string',
            Value=parameter_value,
            Type='String',
            # KeyId='string',
            Overwrite=True,
            # AllowedPattern='string',
            Tier='Standard',
            # Policies='string',
            DataType='text'
        )

    def get_dict_ssm_parameter(self, parameter_name):

        try:
            response = self.ssm_client.get_parameter(
                Name=parameter_name,
            )
            value = json.loads(response["Parameter"]["Value"])
        except self.ssm_client.exceptions.ParameterNotFound as e:
            value = "参数不存在"
        except Exception as e:
            raise e

        return value

    def get_str_ssm_parameter(self, parameter_name):

        response = self.ssm_client.get_parameter(
            Name=parameter_name,
        )
        value = response["Parameter"]["Value"]

        return value

    def delete_parameter(self, parameter_name):

        response = self.ssm_client.delete_parameter(
            Name=parameter_name
        )
