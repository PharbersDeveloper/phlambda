import constants.Common as Common
from handler.Command.Receiver import Receiver


class ClearCKReceiver(Receiver):

    def __init__(self):
        self.clickhouse = Common.EXTERNAL_SERVICES["clickhouse"]

    def exec(self, data):
        table_name = data["tableName"]
        version = data.get("version", "")
        sql = f"""ALTER TABLE `{table_name}` DELETE WHERE 1 = 1"""
        if version != "" and version is not None:
            sql = sql + f""" and version = '{version}'"""

        self.clickhouse.exec_ddl_sql(sql)
