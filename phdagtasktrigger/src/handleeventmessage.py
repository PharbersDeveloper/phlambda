import json
import requests
import boto3


class HandleTaskMessage:

    def __init__(self, ssm_dict, msg):
        self.ssm_dict = ssm_dict
        self.msg = msg
        self.project_name = self.msg.get("project_name", "max")
        self.flow_version = self.msg.get("flow_version", "developer")
        self.dag_run_id = self.msg.get("run_id", "ETL_Iterator_ETL_Iterator_developer_2021-12-15T05:09:13+00:00")
        self.task_id = self.msg.get("task_id", "ETL_Iterator_ETL_Iterator_developer_compute_vvv_r1cjJ3Kz7yGyLv1")
        self.execution_date = self.dag_run_id[self.dag_run_id.rfind("_") + 1:]
        self.dag_id = "_".join([self.project_name, self.project_name, self.flow_version])
        self.clear_task_cat = self.msg.get("clean_cat", "self_only")  # self_only, upstream, downstream

    def clearTaskInstances(self, project_name, dag_id, clean_tasks, execution_date):
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        airflow_url = self.ssm_dict.get(project_name)
        url = "http://" + airflow_url + "/api/v1/dags/" + dag_id + "/clearTaskInstances"
        print("clearTaskInstances的 url")
        print(url)
        # url = "http://" + url + "/api/v1/dags/" + dag_id
        body = {
            "dry_run": False,
            "task_ids": clean_tasks,
            "start_date": execution_date,
            "end_date": execution_date,
            "only_failed": False,
            "only_running": False,
            "include_subdags": True,
            "include_parentdag": True,
            "reset_dag_runs": True
        }
        print(body)
        result = requests.post(url=url, data=json.dumps(body), headers=headers)
        print(result)
        if result.status_code != 200:
            raise Exception()

        return

    def updateTaskInstancesState(self, project_name, dag_id, task_id, execution_date, is_downstream, is_upstream):
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        # 1. 第一步先全部改成success, 这样做的原因在于，将所有的下线全部统一一个状态
        # url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/clearTaskInstances"
        airflow_url = self.ssm_dict.get(project_name)
        url = "http://" + airflow_url + "/api/v1/dags/" + dag_id + "/updateTaskInstancesState"
        print("updateTaskInstancesState url")
        print(url)
        # url = "http://" + url + "/api/v1/dags/" + dag_id
        body = {
            "dry_run": False,
            "task_id": task_id,
            "include_future": False,
            "include_past": False,
            "include_upstream": is_upstream,
            "include_downstream": is_downstream,
            "new_state": "success",
            "execution_date": execution_date
        }

        result = requests.post(url=url, data=json.dumps(body), headers=headers)
        if result.status_code != 200:
            raise Exception()

        # 2. 第一步先全部改成failed, 这样做的原因在于, 能一次性得到所有的下线或上线的task_id
        body = {
            "dry_run": False,
            "task_id": task_id,
            "include_future": False,
            "include_past": False,
            "include_upstream": is_upstream,
            "include_downstream": is_downstream,
            "new_state": "failed",
            "execution_date": execution_date
        }
        result = requests.post(url=url, data=json.dumps(body), headers=headers)
        if result.status_code != 200:
            raise Exception()

        task_instances = result.json()['task_instances']
        reVal = []
        for ins in task_instances:
            reVal.append(ins["task_id"])

        print(reVal)
        return reVal

    def delete_dy_item(self,item):
        run_id = item["run_id"]
        task_ids = item["task_ids"]
        dynamodb_resource = boto3.resource('dynamodb')
        table = dynamodb_resource.Table("notification")
        for tid in task_ids:
            table.delete_item(
                Key = {
                    "id": run_id,
                    "projectId": tid
                }
            )

    def handle_retry_process(self):

        print("进入retry流程1148")
        try:
            clean_tasks = [self.task_id]
            if self.clear_task_cat != "self_only":
                clean_tasks = self.updateTaskInstancesState(self.project_name, self.dag_id, self.task_id, self.execution_date,
                                                       is_upstream=True if self.clear_task_cat == "upstream" else False,
                                                       is_downstream=True if self.clear_task_cat == "downstream" else False)

            print("clean的task")
            print(clean_tasks)
            self.delete_dy_item({
                "run_id": self.dag_run_id,
                "task_ids": clean_tasks
            })
            self.clearTaskInstances(self.project_name, self.dag_id, clean_tasks, self.execution_date)
            res = {
                "status": "success",
                "data": {
                    "execution_date": self.execution_date,
                    "project_name": self.project_name,
                    "flow_version": self.flow_version,
                    "task_id": self.task_id,
                    "clean_cat": self.clear_task_cat
                }
            }
        except Exception as e:
            print(str(e))
            res = {
                "status": "error",
                "data": {
                    "execution_date": self.execution_date,
                    "project_name": self.project_name,
                    "flow_version": self.flow_version,
                    "task_id": self.task_id,
                    "clean_cat": self.clear_task_cat
                },
                "message": "something wrong"
            }
        return res

