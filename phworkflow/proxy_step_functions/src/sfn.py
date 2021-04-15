import boto3
import os
import json
import uuid

DEFAULT_ROLE_ARN = 'arn:aws-cn:iam::444603803904:role/Pharbers-IoC-Maintainer'
DEFAULT_MACHINE_TYPE = 'STANDARD'

class Sfn(object):
    def __init__(self):
        self.client = boto3.client('stepfunctions')

    def create_sfn(self, event):
        """
            创建step_functions
            param definition: 创建step_functions的json
        """
        response = self.client.create_state_machine(
            name=event['create_machine_name'],
            definition=json.dumps(event['definition']),
            roleArn=event.get('role_arn', DEFAULT_ROLE_ARN),
            type=event.get('machine_type', DEFAULT_MACHINE_TYPE),
        )
        return response

    def run_sfn(self, event):

        response = self.client.start_execution(
            stateMachineArn=event['machine_arn'],
            name=event.get('run_machine_name', str(uuid.uuid4())),
            input=json.dumps(event.get('machine_input', {}))
        )
        return response


if __name__ == '__main__':

    event = {
        "machine_arn": "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:hbzhao_test",
        "machine_name": "hbzhao_test",
        "roleArn": "arn:aws-cn:iam::444603803904:role/Pharbers-IoC-Maintainer",
        "type": "STANDARD",
        "definition": {
            "Comment": "An example of the Amazon States Language for running jobs on Amazon EMR",
            "StartAt": "Run first step hbzhao",
            "States": {
                "Run first step hbzhao": {
                    "Type": "Task",
                    "Resource": "arn:aws-cn:states:::elasticmapreduce:addStep.sync",
                    "Parameters": {
                        "ClusterId": "j-311Y2HBZW2J3O",
                        "Step": {
                            "Name": "My first EMR step",
                            "ActionOnFailure": "CONTINUE",
                            "HadoopJarStep": {
                                "Jar": "command-runner.jar",
                                "Args": ["spark-submit",
                                         "--deploy-mode", "cluster",
                                         "s3://ph-test-emr/health_violations.py",
                                         "--data_source", "s3://ph-test-emr/food_establishment_data.csv",
                                         "--output_uri", "s3://ph-test-emr/myOutputFolder1"]
                            }
                        }
                    },
                    "Retry" : [
                        {
                            "ErrorEquals": [ "States.ALL" ],
                            "IntervalSeconds": 1,
                            "MaxAttempts": 3,
                            "BackoffRate": 2.0
                        }
                    ],
                    "ResultPath": "$.firstStep",
                    "Next": "Run second step hbzhao"
                },
                "Run second step hbzhao": {
                    "Type": "Task",
                    "Resource": "arn:aws-cn:states:::elasticmapreduce:addStep.sync",
                    "Parameters": {
                        "ClusterId": "j-311Y2HBZW2J3O",
                        "Step": {
                            "Name": "My second EMR step",
                            "ActionOnFailure": "CONTINUE",
                            "HadoopJarStep": {
                                "Jar": "command-runner.jar",
                                "Args": ["spark-submit",
                                         "--deploy-mode", "cluster",
                                         "s3://ph-test-emr/health_violations.py",
                                         "--data_source", "s3://ph-test-emr/food_establishment_data.csv",
                                         "--output_uri", "s3://ph-test-emr/myOutputFolder2"]
                            }
                        }
                    },
                    "Retry" : [
                        {
                            "ErrorEquals": [ "States.ALL" ],
                            "IntervalSeconds": 1,
                            "MaxAttempts": 3,
                            "BackoffRate": 2.0
                        }
                    ],
                    "ResultPath": "$.secondStep",
                    "End": True
                }
            }
        }
    }
    sfn = Sfn()
    # response = src.create_sfn(event=event)
    response = sfn.run_sfn(event=event)
    print(response)
