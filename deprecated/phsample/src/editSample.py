import json
import time
import os
import boto3
from util.AWS.DynamoDB import DynamoDB
# from phdydatasource_layer.handler.ExecHandler import makeData
from phprojectargs.projectArgs import ProjectArgs


class EditSample(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.project_message = json.loads(self.item.get("message"))
        self.action_id = self.item.get("id")
        self.jobDesc = self.item.get("jobDesc")
        self.emr_client = boto3.client("emr")
        self.dynamodb = DynamoDB()

    def run_emr_step(self, dag_name, job_full_name, project_id, args_list=None):
        args = ProjectArgs(project_id)
        clusters = args.get_cluster_list()
        for cluster in clusters:
            if cluster.get("type") == "emr":
                cluster_id = cluster.get("id")

        step_name = dag_name + "_" + job_full_name

        step = {}
        step.update({"Name": step_name})
        step.update({"ActionOnFailure": "CONTINUE"})
        step.update({"HadoopJarStep": {}})
        step["HadoopJarStep"].update({"Jar": "command-runner.jar"})
        step["HadoopJarStep"].update({"Args": args_list})
        steps=[]
        steps.append(step)
        run_step_response = self.emr_client.add_job_flow_steps(
            JobFlowId=cluster_id,
            Steps=steps
        )

        while run_step_response:
            print("query emr status")
            time.sleep(30)
            step_information_response = self.emr_client.describe_step(
                ClusterId=cluster_id,
                StepId=run_step_response["StepIds"][0]
            )
            step_statuses = ["COMPLETED", "FAILED", "CANCELLED", "INTERRUPTED"]

            if step_information_response['Step']['Status']['State'] in step_statuses:
                step_id = run_step_response["StepIds"][0]
                step_status = step_information_response['Step']['Status']['State']
                break

        return step_status

    def get_cluster_id(self):
        res = self.emr_client.list_clusters(
            ClusterStates=[
                "WAITING",
                "RUNNING"
            ]
        )
        cluster_ids = list([cluster['Id'] for cluster in res.get('Clusters') if cluster['Name'] =="phdev"])
        return cluster_ids[0]


    def create_step_args(self, dag_name, job_full_name, run_id, parameters):
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

    def put_notification(self, step_status):

        if step_status == "COMPLETED":
            status = "succeed"
            zh_status = "sample????????????"
            en_status = "sample edit success"
        else:
            status = "failed"
            zh_status = "sample????????????"
            en_status = "sample edit failed"

        table_name = "notification"
        item = {}
        message = {
            "type": "notification",
            "opname": self.project_message.get("owner"),
            "cnotification": {
                "status": status,
                "error": json.dumps({
                    "code": "123",
                    "message": {
                        "zh": zh_status,
                        "en": en_status
                    }
                }, ensure_ascii=False)
            }
        }

        item.update({"id": self.action_id})
        item.update({"projectId": self.project_message.get("targetProjectId")})
        item.update({"category": ""})
        item.update({"code": "0"})
        item.update({"comments": ""})
        item.update({"date": str(int(round(time.time() * 1000)))})
        item.update({"jobCat": "notification"})
        item.update({"jobDesc": self.jobDesc})
        item.update({"message": json.dumps(message, ensure_ascii=False)})
        item.update({"owner": self.project_message.get("owner")})
        item.update({"showName": self.project_message.get("showName")})
        item.update({"status": status})
        data = {
            "table_name": table_name,
            "item": item
        }

        self.dynamodb.putData(data)
        # type_name = "put_item"
        # makeData(table_name, body, type_name)

    def execute(self):
        # ???????????? ??????ph_conf
        parameters = {}
        parameters.update({"sourceProjectId": self.project_message.get("sourceProjectId")})
        parameters.update({"targetProjectId": self.project_message.get("targetProjectId")})
        parameters.update({"projectName": self.project_message.get("projectName")})
        parameters.update({"showName": self.project_message.get("showName")})
        parameters.update({"datasetId": self.project_message.get("datasetId")})
        parameters.update({"datasetName": self.project_message.get("datasetName")})
        parameters.update({"datasetVersion": self.project_message.get("datasetVersion")})
        parameters.update({"sample": self.project_message.get("sample")})
        parameters.update({"company": "pharbers"})
        print(parameters)
        dag_name = "sample_developer_dev" if os.getenv("EDITION") == "DEV" else "sample_developer"
        # ??????emr ???????????????
        args = self.create_step_args(dag_name, "sample", time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()), parameters)
        print(args)
        # ??????emr
        step_status = self.run_emr_step("sample_developer", "sample", self.project_message.get("targetProjectId"), args)
        # put_notification
        self.put_notification(step_status)
        pass

