from handler.Command.Receiver import Receiver
from constants.Errors import SchemaNotMatched, ColumnDuplicate
import logging


class CheckSchemaReceiver(Receiver):

    def __init__(self):
        pass

    def check(self, data):
        logging.debug("Alex Check Schema ====> \n")
        cur_schema = list(map(lambda item: item["src"], data["cur_schema"]))
        ds_schema = list(map(lambda item: item["src"], data["ds_schema"]))
        if len(set(ds_schema) - set(cur_schema)) > 0:  # 检测 Schema 在多次上传时是否与以前一直
            raise SchemaNotMatched("Schema Not Matched")

        if len(cur_schema) != len(set(cur_schema)):  # 检测 Schema 中是否有重复的列
            raise ColumnDuplicate("Duplicate Column Names")
