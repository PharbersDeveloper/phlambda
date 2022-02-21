from constants.Errors import Errors, FileNotFound, NotXlsxFile, SchemaNotMatched, VersionAlreadyExist, ColumnDuplicate
from handler.Strategy.Strategy import Strategy
from openpyxl.utils.exceptions import InvalidFileException

from handler.Command.CheckSchemaReceiver import CheckSchemaReceiver
from handler.Command.CheckCommand import CheckSchemaConsistencyCommand
from handler.Command.DagReceiver import DagReceiver
from handler.Command.DataSetReceiver import DataSetReceiver
from handler.Command.SaveCommand import SaveDataSetCommand, SaveDagCommand
from handler.Command.MsgReceiver import MsgReceiver
from handler.Command.SendMsgCommand import SendMsgRunCommand
from boto3.dynamodb.conditions import Attr
from util.execl import Excel
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL

import os
import re
import json
import constants.DefinValue as DV
import constants.Common as Common


class Xlsx(Strategy):
    parameters = None

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        self.clickhouse = Common.EXTERNAL_SERVICES["clickhouse"]
        self.msg_receiver = MsgReceiver()
        self.logger = PhLogging().phLogger("Excel XLSX TYPE", LOG_DEBUG_LEVEL)

    def __xlsx_callback(self, data, batch_size, hit_count):
        self.logger.debug("Read_Call ===> \n")

        project_id = self.parameters["project_id"]
        version = self.parameters["version"]
        ds_name = self.parameters["ds_name"]
        table_name = f"{project_id}_{ds_name}"
        original_schema = self.parameters["original_schema"]
        standard_schema = self.parameters["standard_schema"]

        cols_description = ",".join(list(map(lambda col: f"""`{re.sub(DV.FILTER_COL_REG, "_", col['des'])}`""",
                                             standard_schema)))

        sql = f"INSERT INTO {os.environ.get(DV.CLICKHOUSE_DB)}.`{table_name}` ({cols_description}) VALUES"

        def add_col(col):
            value = {}
            for x in list(col.keys()):
                mi = list(filter(lambda mapper_item: mapper_item["des"] == x, original_schema))[0]
                fieldType = DV.TYPE_STRUCTURE[mi["type"]]
                value[re.sub(DV.FILTER_COL_REG, "_", x)] = re.sub("[']", "", fieldType(col[x]))
            value["version"] = version
            return value

        def remove_none_value(lines):
            values = list(filter(lambda line: len(set(line.values())) != 1 or
                                              (len(set(line.values())) == 1 and set(line.values()).pop() is not None),
                                 lines))
            return values

        hit_value = 100 / batch_size
        progress = round(float(hit_count * hit_value), 2)
        self.logger.debug(f"progress ====> {progress} \n")

        if progress == 100:
            data = remove_none_value(data)

        self.logger.debug(f"sql ====> \n {sql}")
        execl_data = list(map(add_col, data))
        self.clickhouse.insert_data(sql, execl_data)

        # 主要做写入Notification操作的进度
        message = dict({}, **self.parameters)
        message["data"] = {"progress": progress}
        SendMsgRunCommand(self.msg_receiver).execute(message)

    def __write2Clickhouse(self):
        self.logger.debug("write2Clickhouse \n")
        project_id = self.parameters["project_id"]
        skip_first = self.parameters["skip_first"]
        skip_next = self.parameters["skip_next"]
        version = self.parameters["version"]
        file_name = self.parameters["file_name"]
        sheet_name = self.parameters["sheet_name"]
        ds_name = self.parameters["ds_name"]
        table_name = f"{project_id}_{ds_name}"
        original_schema = self.parameters["original_schema"]
        standard_schema = self.parameters["standard_schema"]
        fields = ", ".join(
            list(map(lambda field: f"""`{field['des']}` {field["type"]}""", standard_schema))
        )

        # Create Table
        create_table_sql = f"CREATE TABLE IF NOT EXISTS " \
                           f"{os.environ.get(DV.CLICKHOUSE_DB)}.`{table_name}` " \
                           f"({fields}) ENGINE=MergeTree() PRIMARY KEY version"
        self.logger.debug(f"create table ====> \n {create_table_sql}")
        self.clickhouse.exec_ddl_sql(create_table_sql)

        # Check Version
        count_sql = f"SELECT COUNT(1) FROM " \
                    f"{os.environ.get(DV.CLICKHOUSE_DB)}.`{table_name}` " \
                    f"WHERE version = '{version}'"
        self.logger.debug(f"count sql ====> \n  {count_sql}")
        count = self.clickhouse.get_count(count_sql)
        if count > 0:
            raise VersionAlreadyExist("version already exist")

        Excel(
            f"{os.environ[DV.FILE_PATH]}{file_name}", sheet_name,
            skip_first + 1, skip_next,
            original_schema, int(os.environ.get(DV.BATCH_SIZE, 10000))
        ).batchReader(self.__xlsx_callback)

    def do_exec(self, data):
        self.logger.debug("Excel Xlsx ====> \n")

        try:
            # TODO 应该在抽象一层参数类,以Build构造出数据，第一版本先这样
            parameters = {
                "id": data["id"],
                "owner": data["owner"],
                "showName": data["showName"],
                "project_id": data["projectId"],
                "skip_first": data["message"]["skipValue"],
                "skip_next": data["message"]["jumpValue"],
                "version": data["message"].get("version", "0.0.0"),
                "file_name": data["message"]["fileId"],
                "sheet_name": data["message"]["fileSheet"],
                "ds_name": data["message"]["destination"],
                "opgroup": data["message"]["opgroup"],
                "cat": data["message"].get("cat", "intermediate"),
                "path": data["message"].get("path", ""),
                "prop": data["message"].get("prop", ""),
                "format": data["message"].get("format", ""),
                "prefix": data["jobDesc"],
                "jobCat": "project_file_to_DS_"
            }

            self.parameters = parameters

            original_schema = list(map(
                lambda item: {"src": item, "des": item, "type": "String"},
                data.get("mapper", Excel.getSchema(os.environ[DV.FILE_PATH] + parameters["file_name"],
                                                   parameters["sheet_name"],
                                                   int(parameters["skip_first"]) + 1))
            ))

            standard_schema = list(map(lambda item: {
                "src": re.sub(DV.FILTER_COL_REG, "_", item["src"]),
                "des": re.sub(DV.FILTER_COL_REG, "_", item["des"]),
                "type": item["type"]
            }, original_schema))
            if "version" not in standard_schema:
                standard_schema = standard_schema + [{"src": "version", "des": "version", "type": "String"}]

            ds_result = self.dynamodb.scanTable({
                "table_name": "dataset",
                "limit": 100000,
                "expression": Attr("name").eq(parameters["ds_name"]) & Attr("projectId").eq(parameters["project_id"]),
                "start_key": ""
            })["data"]

            ds_id = parameters["file_name"]
            label = "[]"
            if len(ds_result) > 0:
                ds_id = ds_result[0]["id"]
                label = ds_result[0]["label"]

            parameters["original_schema"] = original_schema
            parameters["standard_schema"] = standard_schema
            parameters["ds_id"] = ds_id
            parameters["label"] = label

            CheckSchemaConsistencyCommand(CheckSchemaReceiver()).execute({
                "cur_schema": standard_schema,
                "ds_schema": json.loads(ds_result[0]["schema"]) if len(ds_result) > 0 else []
            })

            self.__write2Clickhouse()  # 写数据
            SaveDataSetCommand(DataSetReceiver()).execute(parameters)  # 建DynamoDB Dataset索引
            self.logger.debug("SaveDataSetCommand")
            SaveDagCommand(DagReceiver()).execute(parameters)  # 写Dag
            self.logger.debug("SaveDagCommand")

        except FileNotFoundError as e:
            raise FileNotFound(e)
        except InvalidFileException as e:
            raise NotXlsxFile(e)
        except VersionAlreadyExist as e:
            raise e
        except SchemaNotMatched as e:
            raise e
        except ColumnDuplicate as e:
            raise e
        except Exception as e:
            raise Errors(e)

        return self.parameters
