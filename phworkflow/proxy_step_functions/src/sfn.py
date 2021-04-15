import boto3
import os
import json
import uuid

DEFAULT_MACHINE_TYPE = 'STANDARD'
DEFAULT_MACHINE_ARN_SUFFIX = 'arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:'

class Sfn(object):
    def __init__(self):
        self.client = boto3.client('stepfunctions')

    def create_sfn(self, event):
        """
            创建step_functions stateMachine
            param definition: 创建step_functions的json
        """
        response = self.client.create_state_machine(
            name=event['machine_name'],
            definition=json.dumps(event['definition']),
            roleArn=os.getenv("DEFAULT_ROLE_ARN"),
            type=event.get('machine_type', DEFAULT_MACHINE_TYPE),
        )
        return response

    def run_sfn(self, event):
        """
            运行step_functions
            param definition: 创建step_functions的json
        """
        response = self.client.start_execution(
            stateMachineArn=event.get('machine_arn', DEFAULT_MACHINE_ARN_SUFFIX + event['machine_name']),
            name=event.get('perform_name', str(uuid.uuid4())),
            input=json.dumps(event.get('machine_input', {}))
        )
        return response

