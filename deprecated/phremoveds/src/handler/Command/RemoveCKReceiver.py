import os
import constants.Common as Common
import constants.DefinValue as DV
from handler.Command.Receiver import Receiver
from clickhouse_driver.errors import ServerException
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL


class RemoveCKReceiver(Receiver):

    def __init__(self):
        self.logger = PhLogging().phLogger("Remove ClickHouse", LOG_DEBUG_LEVEL)

    def exec(self, data):
        try:
            tableName = f"""{data["projectId"]}_{data["destination"]}"""
            clickhouse = Common.EXTERNAL_SERVICES["clickhouse"](data["projectId"])
            clickhouse.exec_ddl_sql(f"""DROP TABLE {os.environ[DV.CLICKHOUSE_DB]}.`{tableName}`""")
        except ServerException as e:
            if e.code == 60 and "doesn't exist" in e.message:
                self.logger.debug("table 没有找到")
        except Exception as e:
            raise e
