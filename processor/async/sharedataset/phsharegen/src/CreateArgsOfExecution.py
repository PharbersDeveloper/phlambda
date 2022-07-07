import json




def create_args_of_execution(execute_py, phmain_py, shareProject, *args, **kwargs):

    event = kwargs
    args_of_execution = {
        "common": {
            "runnerId": event["common"]["runnerId"],
            "projectId": event["common"]["projectId"],
            "projectName": event["common"]["projectName"],
            "owner": event["common"]["owner"],
            "showName": event["common"]["showName"]
        },
        "compute_share": {
            "name": "compute_share",
            "type": "spark-submit",
            "clusterId": event["engine"]["id"],
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": [
                    "spark-submit",
                    "--deploy-mode",
                    "cluster",
                    "--conf",
                    "spark.driver.cores=1",
                    "--conf",
                    "spark.driver.memory=1g",
                    "--conf",
                    "spark.executor.cores=1",
                    "--conf",
                    "spark.executor.memory=1g",
                    "--conf",
                    "spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
                    "--conf",
                    "spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
                    "--py-files",
                    f"s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-4.0.0-py3.8.egg,{execute_py}",
                    phmain_py,
                    "--owner",
                    "dev环境",
                    "--dag_name",
                    "sample_sample_developer",
                    "--run_id",
                    event["runnerId"],
                    "--job_full_name",
                    "sample_sample_developer_compute_share",
                    "--tenant_ip",
                    event["engine"]["dss"]["ip"],
                    "--ph_share",
                    json.dumps({"ph_share": event["share"],
                                "shareProject":str(shareProject)}, ensure_ascii=False).replace("}}", "} }").replace("{{", "{ {"),
                ]
            }
        }
    }

    return args_of_execution



