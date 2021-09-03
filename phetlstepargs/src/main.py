import json
import time


def lambda_handler(event, context):
    # TODO implement
    index = event['iterator']['index'] -1
    parameters = event['parameters']
    parameter = parameters[index]
    allow_type = ['csv','xml','json','parquet']
    type = parameter['type']
    if type.lower() in allow_type:
        args = ["spark-submit",
                "--deploy-mode", "cluster",
                "--conf", "spark.driver.cores=1",
                "--conf", "spark.driver.memory=1g",
                "--conf", "spark.executor.cores=1",
                "--conf", "spark.executor.memory=1g",
                "--conf", "spark.executor.instances=1",
                "--conf", "spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
                "--conf", "spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
                "--py-files",
                "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-3.0.7-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/readable/for_readable_move_to_readable/phjob.py",
                "s3://ph-platform/2020-11-11/jobs/python/phcli/readable/for_readable_move_to_readable/phmain.py",
                "--owner", "default_owner",
                "--dag_name", "readable",
                "--run_id", "readable_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()),
                "--job_full_name", "for_readable_move_to_readable",
                "--job_id", "not_implementation"
                ]

        parameter.pop("type",None)
        for key in parameter.keys():
            args.append("--" + key)
            args.append(parameter[key])

        next_step = "move-to-readable"
    else:
        if type.lower() == "xlsx":
            args = parameter
            next_step = "start_glue_job"
        else:
            raise Exception("Job类型错误")

    return {
        "next_step": next_step,
        "args": args
    }