from handler.Command.Receiver import Receiver
from constants.Errors import SchemaNotMatched, ColumnDuplicate
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL
from collections import Counter


class CheckSchemaReceiver(Receiver):

    def __init__(self):
        self.logger = PhLogging().phLogger("CheckSchema", LOG_DEBUG_LEVEL)

    def check(self, data):
        self.logger.debug(f"Alex Check Schema ====> \n {data}")
        cur_schema = list(map(lambda item: item["src"], data["cur_schema"]))
        ds_schema = list(map(lambda item: item["src"], data["ds_schema"]))
        if len(ds_schema) > 0 and (len(set(ds_schema)) - len(set(cur_schema))) != 0:  # 检测 Schema 在多次上传时是否与以前一直
            raise SchemaNotMatched("Schema Not Matched")

        lower_cur_schema = list(map(lambda item: item.lower(), cur_schema))
        duplicate_col = [key for key, value in dict(Counter(lower_cur_schema)).items()if value > 1]
        if len(duplicate_col) > 0:  # 检测 Schema 中是否有重复的列
            cols = ",".join(duplicate_col)
            raise ColumnDuplicate(cols)
