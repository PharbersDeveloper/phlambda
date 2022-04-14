import os
import json
import time
import constants.Common as Common
from handler.Command.SaveCommand import SaveCommand
from handler.Command.RemoveJobReceiver import RemoveJobReceiver
from constants.Errors import Errors


class RemoveJob:

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]

    def exec(self, item):
        try:
            messages = item["message"]
            for message in messages:
                SaveCommand(RemoveJobReceiver()).execute({
                    "project_id": item["projectId"],
                    "target_id": message["targetId"],
                    "job_name": message["jobName"],
                    "flow_version": message["flowVersion"]
                })

            suffix = ""
            if os.environ["EDITION"] == "DEV":
                suffix = "_dev"
            self.dynamodb.putData({
                "table_name": "action" + suffix,
                "item": {
                    "projectId": item["projectId"],
                    "code": 0,
                    "comments": "dag_refresh",
                    "date": str(int(round(time.time() * 1000))),
                    "jobCat": "dag_refresh",
                    "jobDesc": "refresh",
                    "message": json.dumps({
                        "projectId": item["projectId"],
                        "flowVersion": messages[0]["flowVersion"] if len(messages) > 0 else "developer",
                        "jobCat": "dag_refresh",
                        "opname": item["owner"],
                        "projectName": messages[0].get("projectName", "") if len(messages) > 0 else ""
                    }),
                    "owner": item["owner"],
                    "showName": item["showName"]
                }
            })

        except Exception as e:
            raise Errors(e)
