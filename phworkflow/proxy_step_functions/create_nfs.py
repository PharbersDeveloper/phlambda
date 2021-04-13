import boto3
import json

client = boto3.client('stepfunctions')

definition = {
    "Comment": "An example of the Amazon States Language for running jobs on Amazon EMR",
    "StartAt": "Run first step",
    "States": {
        "Run first step": {
            "Type": "Task",
            "Resource": "arn:aws-cn:states:::elasticmapreduce:addStep.sync",
            "Parameters": {
                "ClusterId": "j-2I9FR1U969A4J",
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
            "Next": "Run second step"
        },
        "Run second step": {
            "Type": "Task",
            "Resource": "arn:aws-cn:states:::elasticmapreduce:addStep.sync",
            "Parameters": {
                "ClusterId": "j-2I9FR1U969A4J",
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

response = client.create_state_machine(
    name='clock_name',
    definition=json.dumps(definition),
    roleArn='arn:aws-cn:iam::444603803904:role/Pharbers-IoC-Maintainer',
    type='STANDARD',
    # loggingConfiguration={
    #     'level': 'ALL'|'ERROR'|'FATAL'|'OFF',
    #     'includeExecutionData': True|False,
    #     'destinations': [
    #         {
    #             'cloudWatchLogsLogGroup': {
    #                 'logGroupArn': 'string'
    #             }
    #         },
    #     ]
    # },
    # tags=[
    #     {
    #         'key': 'string',
    #         'value': 'string'
    #     },
    # ],
    # tracingConfiguration={
    #     'enabled': True|False
    # }
)
