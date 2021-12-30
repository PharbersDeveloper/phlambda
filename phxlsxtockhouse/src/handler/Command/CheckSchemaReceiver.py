from handler.Command.Receiver import Receiver
from constants.Errors import SchemaNotMatched
import logging


class CheckSchemaReceiver(Receiver):

    def __init__(self):
        pass

    def check(self, data):
        logging.debug("Alex Check Schema ====> \n")
        cur_schema = set(map(lambda item: item["src"], data["cur_schema"]))
        ds_schema = set(map(lambda item: item["src"], data["ds_schema"]))
        if len(ds_schema - cur_schema) > 0:
            raise SchemaNotMatched("Schema Not Matched")

