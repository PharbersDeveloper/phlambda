import json
from util.AWS.DynamoDB import DynamoDB


class EditSample(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.dynamodb = DynamoDB()

    def run_emr_step(dag_name, job_full_name, args_list=None):
        cluster_id = get_cluster_id()
        step_name = dag_name + "_" + job_full_name

        step = {}
        step.update({"Name": step_name})
        step.update({"ActionOnFailure": ACTIONONFAILURE})
        step.update({"HadoopJarStep": {}})
        step["HadoopJarStep"].update({"Jar": STEP_JAR})
        step["HadoopJarStep"].update({"Args": args_list})
        steps=[]
        steps.append(step)
        run_step_response = emr_client.add_job_flow_steps(
            JobFlowId=cluster_id,
            Steps=steps
        )

        while run_step_response:
            time.sleep(30)
            step_information_response = emr_client.describe_step(
                ClusterId=cluster_id,
                StepId=run_step_response["StepIds"][0]
            )
            step_statuses = ["COMPLETED", "FAILED", "CANCELLED", "INTERRUPTED"]

            if step_information_response['Step']['Status']['State'] in step_statuses:
                step_id = run_step_response["StepIds"][0]
                step_status = step_information_response['Step']['Status']['State']
                break

        emr_log = "s3://ph-platform/2020-11-11/emr/logs/" + cluster_id + "/steps/" + step_id + "/"

        return {
            "emr_log": emr_log,
            "step_status": step_status
        }

    def get_cluster_id():
        res = emr_client.list_clusters(
            ClusterStates=[
                "WAITING",
                "RUNNING"
            ]
        )
        cluster_ids = list([cluster['Id'] for cluster in res.get('Clusters') if cluster['Name'] =="phdev"])
        return cluster_ids[0]


    def create_step_args(self, dag_name, job_full_name, run_id):
        args = ["spark-submit",
                "--deploy-mode", "cluster",
                "--conf", "spark.driver.cores=1",
                "--conf", "spark.driver.memory=1g",
                "--conf", "spark.executor.cores=1",
                "--conf", "spark.executor.memory=1g",
                "--conf", "spark.executor.instances=1",
                "--conf", "spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
                "--conf", "spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
                "--jars", "s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/clickhouse-jdbc-0.2.4.jar,s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/guava-30.1.1-jre.jar",
                "--py-files",
                "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-4.0.0-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/phjob.py",
                "s3://ph-platform/2020-11-11/jobs/python/phcli/"+dag_name+"/"+job_full_name+"/phmain.py",
                "--owner", "default_owner",
                "--dag_name", dag_name,
                "--run_id", run_id,
                "--job_full_name", job_full_name,
                "--ph_conf", json.dumps(parameters, ensure_ascii=False).replace("}}", "} }").replace("{{", "{ {"),
                "--job_id", "not_implementation"
                ]

        return args

    def put_notification(self):

        pass

