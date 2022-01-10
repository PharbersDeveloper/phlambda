import os
import constants.Common as Common
import constants.DefinValue as DV
from handler.Command.Receiver import Receiver
from clickhouse_driver.errors import ServerException


class RemoveCKReceiver(Receiver):

    def __init__(self):
        self.clickhouse = Common.EXTERNAL_SERVICES["clickhouse"]

    def exec(self, data):
        try:
            self.clickhouse.exec_ddl_sql(f"""DROP TABLE {os.environ[DV.CLICKHOUSE_DB]}.`{data["tableName"]}`""")
        except ServerException as e:
            if e.code == 60 and "doesn't exist" in e.message:
                print("table 没有找到")
        except Exception as e:
            raise e
