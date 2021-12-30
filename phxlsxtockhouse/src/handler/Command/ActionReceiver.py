from handler.Command.Receiver import Receiver
import constants.Common as Common
import logging


class ActionReceiver(Receiver):

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]

    def save(self, data):
        logging.debug("Alex Save Action ====> \n")

        self.dynamodb.putData({
            "table_name": "action",
            "item": data
        })
