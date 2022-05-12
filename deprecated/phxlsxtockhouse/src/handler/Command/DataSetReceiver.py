from handler.Command.Receiver import Receiver
import constants.Common as Common
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL
import time
import json


class DataSetReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.logger = PhLogging().phLogger("DataSet", LOG_DEBUG_LEVEL)

    def save(self, data):
        self.logger.debug(f"Alex Save DataSet ====> \n  {data}")

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
                "prop": data["prop"],
                "format": data["format"],
                "version": data["version"]
            }
        })
