import json
import requests
import datetime
import traceback


class HandleEventMessage:

    def __init__(self, ssm_dict, msg):
        self.msg = msg
        self.project_name = self.msg.get("project_name", "max")
        self.flow_version = self.msg.get("flow_version", "developer")
        self.conf = self.msg.get("conf", {})
        self.dag_id = "_".join([self.project_name, self.project_name, self.flow_version])

        self.url = ssm_dict.get(self.project_name)
        print(self.url)
        self.res = {}
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }

    def handle_dag_id(self):
        # 如果存在dag_id将状态改为激活
        # update_url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id
        update_url = "http://" + self.url + "/api/v1/dags/" + self.dag_id
        try:
            body = {"is_paused": False}
            result = requests.patch(url=update_url, data=json.dumps(body), headers=self.headers)
            if result.status_code != 200:
                self.res["status"] = "failed"
                self.res["msg"] = self.dag_id + " Activation failed"
        except:
            self.res["status"] = "failed"
            self.res["msg"] = update_url + "api error"

    def handle_run_status(self):
        # dag_id状态激活后即可开始run
        # runs_url = "https://max.pharbers.com/airflow/api/v1/dags/" + dag_id + "/dagRuns"
        runs_url = "http://" + self.url + "/api/v1/dags/" + self.dag_id + "/dagRuns"

        try:
            execution_date = datetime.datetime.utcnow()
            # dag_run_id = "_".join([project_name, dag_id, flow_version])
            dag_run_id = "_".join([self.project_name, self.project_name, self.flow_version, execution_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")])
            body = {
                "dag_run_id": dag_run_id,
                "execution_date": execution_date.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "conf": self.conf
            }
            dag_runs = requests.post(url=runs_url, data=json.dumps(body), headers=self.headers)
            if dag_runs.status_code == 200:
                airflow_result = dag_runs.json()
                self.res["status"] = "success"
                self.res["data"] = {
                    "dag_run_id": airflow_result["dag_run_id"],
                    "dag_id": airflow_result["dag_id"],
                    "run_id": dag_run_id,
                    "project_name": self.project_name
                }
            else:
                self.res["status"] = "failed"
                self.res["msg"] = self.dag_id + " Trigger failure"
        except:
            print(traceback.format_exc())
            self.res["status"] = "failed"
            self.res["msg"] = runs_url + " api error"
