from handler.Command.Receiver import Receiver
import constants.Common as Common
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class ActionReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.logger = PhLogging().phLogger("Action", LOG_DEBUG_LEVEL)

    def save(self, data):
        self.logger.debug(f"Alex Save Action ====> \n {data}")

        self.dynamodb.putData({
            "table_name": "action",
            "item": data
        })
