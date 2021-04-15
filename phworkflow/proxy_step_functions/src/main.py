from src.sfn import Sfn

def lambda_handler(event, context):

    sfn = Sfn()
    if event['policy'] == 'CreateAndRun':
        create_response = sfn.create_sfn(event)
        print(create_response)
        machine_arn = create_response.get('stateMachineArn')
        event['machine_arn'] = machine_arn
        run_response = sfn.run_sfn(event)
        print(run_response)
    elif event['policy'] == 'Create':
        response = sfn.create_sfn(event)
        print(response)
    elif event['policy'] == 'Run':
        response = sfn.run_sfn(event)
        print(response)


if __name__ == '__main__':

    event = {
        "policy": "Run",
        "machine_arn": "arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:hbzhao_test",
        "create_machine_name": "hbzhao_test",
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
    # response = lambda_handler(event=event)
    lambda_handler(event=event, context=None)

# spark-submit --master yarn --deploy-mode cluster
# --name autodatamatchnewcodetestdatamatchingcleaningdatanormalization-f
# --proxy-user airflow --queue airflow
# --conf spark.driver.cores=1 --conf spark.driver.memory=3g
# --conf spark.executor.cores=4 --conf spark.executor.memory=2g
# --conf spark.executor.instances=4 --conf spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Dcom.amazonaws.services.s3.enableV4
# --conf spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Dcom.amazonaws.services.s3.enableV4
# --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem
# --conf spark.hadoop.fs.s3a.access.key=AKIAWPBDTVEANRUMG5P6
# --conf spark.hadoop.fs.s3a.secret.key=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
# --conf spark.hadoop.fs.s3a.endpoint=s3.cn-northwest-1.amazonaws.com.cn
# --conf jars=s3a://ph-platform/2020-11-11/jobs/python/phcli/common/aws-java-sdk-bundle-1.11.828.jar,s3a://ph-platform/2020-11-11/jobs/python/phcli/common/hadoop-aws-3.2.1.jar
# --conf spark.sql.codegen.wholeStage=False
# --conf spark.sql.execution.arrow.pyspark.enable=true
# --conf spark.sql.crossJoin.enabled=true
# --conf spark.sql.autoBroadcastJoinThreshold=-1
# --conf spark.sql.files.maxRecordsPerFile=554432
# --py-files s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-2.2.1-py3.8.egg,s3://ph-test-emr/phjob.py
# s3://ph-platform/2020-11-11/jobs/python/phcli/Auto_data_match_newcode_test/data_matching_cleaning_data_normalization/phmain.py
#
# --owner mzhang --run_id manual__testyear-04-08T00_47_13.535678+00_00 --job_id testdatamatchnewcodetestdatamatchingcleaningdatanormalization-f --job_name cleaning_data_normalization --path_prefix s3://ph-max-auto/2020-08-11/data_matching/refactor/runs --path_cleaning_data s3://ph-max-auto/2020-08-11/data_matching/refactor/data/CHC/* --path_human_interfere s3://ph-max-auto/2020-08-11/data_matching/refactor/data/HUMAN_INTERFERE --path_second_human_interfere s3://ph-max-auto/2020-08-11/data_matching/refactor/data/DF_CONF/0.3 --source_data_type chc --cleaning_result cleaning_result --cleaning_origin cleaning_origin

