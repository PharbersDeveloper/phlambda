import constants.Common as Common
from handler.Command.Receiver import Receiver


class RemoveCKReceiver(Receiver):

    def __init__(self):
        self.clickhouse = Common.EXTERNAL_SERVICES["clickhouse"]

    def exec(self, data):
        self.clickhouse.exec_ddl_sql(f"""DROP TABLE `{data["tableName"]}`""")
