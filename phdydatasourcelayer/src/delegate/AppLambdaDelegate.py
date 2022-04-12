import json
import re
import handler.ExecHandler as ExecHandler
from models.Execution import Execution
from models.Step import Step
from models.Action import Action
from models.ProjectFile import ProjectFile
from models.Partition import Partition
from models.DataSet import DataSet
from models.Notification import Notification
from models.Dag import Dag
from models.DagConf import DagConf
from models.Log import Log


table_structure = {
    "execution": Execution,
    "step": Step,
    "action": Action,
    "project_files": ProjectFile,
    "partition": Partition,
    "dataset": DataSet,
    "notification": Notification,
    "dag": Dag,
    "dagconf": DagConf,
    "logs": Log
}


class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def exec(self):
        method = self.event.get("httpMethod")
        type = self.event.get("pathParameters").get("type")
        body = json.loads(self.event.get("body"))
        re_type = r"(^query$)|(^scan$)|(^put_item$)|(^delete_item$)"
        re_method = r"^post$"
        if bool(re.match(re_method, method)) & \
           bool(re.match(re_type, type)):
            return {
                "statusCode": 403,
                "headers": {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
                },
                "body": json.dumps({
                    "message": "invalid parameter"
                })
            }

        table = body["table"]

        json_api_data = ExecHandler.makeData(table, body, type, table_structure)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(json_api_data)
        }
