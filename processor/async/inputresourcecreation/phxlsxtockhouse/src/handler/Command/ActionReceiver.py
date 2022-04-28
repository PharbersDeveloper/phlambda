import os
import constants.Common as Common
import constants.DefinValue as DV
from handler.Command.Receiver import Receiver
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class ActionReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.logger = PhLogging().phLogger("Action", LOG_DEBUG_LEVEL)

    def save(self, data):
        dev = "_" + os.environ[DV.DEV].lower() if os.environ[DV.DEV].lower() == "dev" else ""
        self.logger.debug(f"Alex Save Action ====> \n {data}")

        self.dynamodb.putData({
            "table_name": "action" + dev,
            "item": data
        })
