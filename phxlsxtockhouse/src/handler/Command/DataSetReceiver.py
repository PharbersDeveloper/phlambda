from handler.Command.Receiver import Receiver
import constants.Common as Common
import logging
import time
import json


class DataSetReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]

    def save(self, data):
        logging.debug("Alex Save DataSet ====> \n")

        self.dynamodb.putData({
            "table_name": "dataset",
            "item": {
                "id": data["ds_id"],
                "projectId": data["project_id"],
                "date": int(round(time.time() * 1000)),
                "name": data["name"],
                "schema": json.dumps(data["schema"], ensure_ascii=False),
                "label": data["label"],
                "cat": data["cat"],
                "path": data["path"],
                "version": data["version"]
            }
        })
