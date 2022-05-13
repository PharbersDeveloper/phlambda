import os
import constants.Common as Common
import constants.DefinValue as DV
from handler.Command.Receiver import Receiver
from clickhouse_driver.errors import ServerException
from constants.Errors import Errors
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class ClearCKReceiver(Receiver):

    def __init__(self):
        self.logger = PhLogging().phLogger("Clear ClickHouse", LOG_DEBUG_LEVEL)

    def exec(self, data):
        self.logger.debug(f"{data}")
        clickhouse = Common.EXTERNAL_SERVICES["clickhouse"](data["projectId"])
        table_name = f"""{data["projectId"]}_{data["destination"]}"""
        version = data.get("version", "")
        sql = f"""ALTER TABLE {os.environ[DV.CLICKHOUSE_DB]}.`{table_name}` DELETE WHERE 1 = 1"""
        if version != "" and version is not None:
            sql = sql + f""" and version = '{version}'"""
        try:
            clickhouse.exec_ddl_sql(sql)
        except ServerException as e:
            if e.code == 60 and "doesn't exist" in e.message:
                print("table 没有找到")
        except Exception as e:
            raise Errors(e)
