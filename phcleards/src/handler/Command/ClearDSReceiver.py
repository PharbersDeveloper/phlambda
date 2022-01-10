import time
import constants.Common as Common
from handler.Command.Receiver import Receiver
from boto3.dynamodb.conditions import Key


class ClearDSReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]

    def exec(self, data):
        ds_id = data["dsid"]
        result = self.dynamodb.queryTable({
            "table_name": "dataset",
            "limit": 100000,
            "expression": Key("id").eq(ds_id),
            "start_key": ""
        })["data"]
        if len(result) > 0:
            result[0]["version"] = ""
            result[0]["date"] = int(round(time.time() * 1000))
            self.dynamodb.putData({
                "table_name": "dataset",
                "item": result[0]
            })
