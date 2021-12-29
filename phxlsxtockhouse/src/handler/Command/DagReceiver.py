from handler.Command.Receiver import Receiver
import constants.Common as Common
import logging


class DagReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]

    def save(self, data):
        logging.debug("Alex Save Dag ====> \n")

        des_table_name = data["ds_name"]
        dsId = data["ds_id"]

        self.dynamodb.putData({
            "table_name": "dag",
            "item": {
                "id": "",
                "projectId": data["project_id"],
                "sortVersion": f"developer_{dsId}",
                "cat": "dataset",
                "cmessage": "",
                "ctype": "node",
                "flowVersion": "developer",
                "level": "-99999",
                "name": des_table_name,
                "position": """{"x": "0", "y": "0", "z": "0", "w": "0", "h": "0"}""",
                "representId": dsId,
                "runtime": "uploaded"
            }
        })
