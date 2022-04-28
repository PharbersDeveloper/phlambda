
import time
from handler.Command.Receiver import Receiver
import constants.Common as Common
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class VersionReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.logger = PhLogging().phLogger("DAG", LOG_DEBUG_LEVEL)

    def save(self, data):
        self.logger.debug(f"Alex Save Dag ====> \n {data}")

        des_table_name = data["ds_name"]
        dsId = data["ds_id"]
        version = data.get("version")

        self.dynamodb.putData({
            "table_name": "version",
            "item": {
                "id": data["project_id"]+"_"+dsId,
                "name": version,
                "projectId": data["project_id"],
                "datasetId": dsId,
                "date": str(int(time.time() * 1000)),
                "owner": "developer",
            }
        })
