import os
import constants.DefinValue as DV
import constants.Common as Common
from handler.Command.Command import Command


class RollBackCommand(Command):

    def execute(self, data):
        clickhouse = Common.EXTERNAL_SERVICES["clickhouse"](data["projectId"])
        message = data["message"]
        version = data.get("version", "0.0.0")
        tableName = data["projectId"] + "_" + message["destination"]
        sql = f"ALTER TABLE {os.environ.get(DV.CLICKHOUSE_DB)}.`{tableName}` DELETE WHERE version = '{version}'"
        showTables = list(map(lambda table: table[0], clickhouse.exec_ddl_sql("SHOW TABLES")))
        print(showTables)
        if tableName in showTables:
            clickhouse.exec_ddl_sql(sql)

