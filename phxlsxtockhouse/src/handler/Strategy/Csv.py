import constants.DefinValue as DV
from constants.Errors import Errors, FileNotFound, NotXlsxFile, SchemaNotMatched, VersionAlreadyExist, ColumnDuplicate
from handler.Command.DagReceiver import DagReceiver
from handler.Command.DataSetReceiver import DataSetReceiver
from handler.Command.VersionReceiver import VersionReceiver
from handler.Command.SaveCommand import SaveDataSetCommand, SaveDagCommand
from util.AWS.ph_s3 import PhS3
import pandas as pd
import boto3
from boto3.dynamodb.conditions import Attr
import os
import re
from clickhouse_driver import Client
import constants.Common as Common
import json


class Csv:
    clickhouse = None
    parameters = None
    write_once = None

    def __init__(self):
        self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        # self.msg_receiver = MsgReceiver()
        # self.logger = PhLogging().phLogger("Excel XLSX TYPE", LOG_DEBUG_LEVEL)
        self.file_name_list = []
        self.schema = None
        self.whileonce = True
        self.clickhouse_client = None
        self.PhS3 = PhS3()
        self.dynamodb_resource = boto3.resource("dynamodb")

    def __create_clickhouse(self, projectId):
        self.clickhouse_client = Common.EXTERNAL_SERVICES["clickhouse"](projectId)

    def parse_data(self, data: list):
        print(data)
        # return list(map(lambda x: dict(zip(self.schema+["version"], x)), [i + [version] for i in data]))
        return list(map(lambda x: dict(zip(self.schema, x)),
                        [[str(j) if str(j) != "nan" else "None" for j in i] for i in data]))

    def createClickhouTableSql(self, table_name, database='default', order_by='', partition_by='version'):
        print(table_name)

        def getSchemeSql():
            sql_scheme = ""
            for i in self.schema:
                sql_scheme += f"`{i}` String,"
            sql_scheme = re.sub(r",$", "", sql_scheme)
            return sql_scheme

        return f"CREATE TABLE IF NOT EXISTS {database}.`{table_name}` ({getSchemeSql()}) ENGINE=MergeTree() PRIMARY KEY version"

    def toS3(self, path, key):
        print(key)
        self.PhS3.upload_dir(path, 'ph-platform', key)

    def do_parquet(self, datal, file_name):
        dataf = pd.DataFrame(datal)
        dataf.columns = self.schema
        dataf.to_parquet(file_name, index=False, partition_cols="version")


    def check_version(self, table_name, version):
        # Check Version
        count_sql = f"SELECT COUNT(1) FROM " \
                    f"{os.environ.get(DV.CLICKHOUSE_DB)}.`{table_name}` " \
                    f"WHERE version = '{version}'"

        count = self.clickhouse.get_count(count_sql)
        if count > 0:
            return True

    def toclickhouse(self, table_name, data, version):
        print("to clickhouse -------------------------")
        print(table_name)
        print(self.schema)
        print(data)
        if len(self.schema) != len(data[0]):
            print("col-----error---------------------")
            return False
        create_sql = self.createClickhouTableSql(table_name)
        print(create_sql)

        self.clickhouse_client.execute(create_sql)
        if self.check_version(table_name, version):
            print("version-----error------------------")
            raise VersionAlreadyExist("version already exist")
        self.clickhouse_client.execute(f'INSERT INTO `{table_name}` VALUES', data)
        return True

    def do_exec(self, data):
        try:
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
                "provider": data["message"].get("provider", "pharbers"),
                "cat": data["message"].get("cat", "intermediate"),
                "path": data["message"].get("path", ""),
                "prop": data["message"].get("prop", ""),
                "format": data["message"].get("format", ""),
                "prefix": data["jobDesc"],
                "ds_id": data["message"]["fileId"],
                "label": "[]",
                "jobCat": "project_file_to_DS_",
            }

            version = parameters.get("version")
            filename = parameters.get("file_name")
            ds_name = parameters.get("ds_name").encode("utf-8").decode()
            projectId = parameters.get("project_id")
            path = f"/mnt/tmp/{projectId}/tmp/{filename}"
            data_list = pd.read_csv(path, chunksize=10000, header=None)
            table_name = f"{projectId}_{ds_name}"
            skip_first = int(parameters.get("skip_first"))
            skip_next = int(parameters.get("skip_next"))
            version = version.encode("utf-8").decode()
            print(skip_next)
            print(skip_first)

            self.__create_clickhouse(projectId)
            out_file_name = f"/mnt/tmp/{projectId}/tmp/pharbers/{projectId}/{ds_name}/"
            for i, dataf in enumerate(data_list):
                dataf["version"] = version
                # dataf1 = dataf.drop(labels=skip,axis=0)
                datal = dataf.values.tolist()


                if self.whileonce:
                    print("not schema insert to clickhouse-------------------")
                    if not skip_first:
                        schemas = [f"col_{count}" if str(col) == "nan" or not col else str(col) for count, col in
                                   enumerate(datal.pop(0))]
                        self.schema = ["version" if schem == version else schem for schem in schemas]
                    if skip_first:
                        print("will to clickhosue-------------------------------------")
                        datal = datal[skip_first:]
                        schemas = [f"col_{count}" if str(col) == "nan" or not col else str(col) for count, col in
                                   enumerate(datal.pop(0))]
                        self.schema = ["version" if schem == version else schem for schem in schemas]
                        print(self.schema)
                    for i in range(skip_next):
                        datal.pop(0)
                    parameters["standard_schema"] = [{"src": sch, "des": sch, "type": "String"} for sch in self.schema]
                    self.whileonce = False
                    new_data = self.parse_data(datal)
                    if not self.toclickhouse(table_name, new_data, version):
                        raise ColumnDuplicate("column duplication")
                    print("toclickhouse--------------success---------------------------------------------------------")
                self.do_parquet(datal, out_file_name)
                print("doparquet--------------success---------------------------------------------------------")
            self.toS3(out_file_name, f"2020-11-11/lake/pharbers/{projectId}/{ds_name}/")

            # TODO: 这个scan要改
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

            parameters["ds_id"] = ds_id
            parameters["label"] = label

            print("success------------------------------------------------------------------------")
            SaveDataSetCommand(DataSetReceiver()).execute(parameters)  # 建DynamoDB Dataset索引
            SaveDagCommand(DagReceiver()).execute(parameters)
            SaveDagCommand(VersionReceiver()).execute(parameters)
            print("dynamodb---------------success--------------------------------------------------")

        except VersionAlreadyExist as e:
            raise e
        except ColumnDuplicate as e:
            raise e
        except Exception as e:
            print(e)
            raise Errors(e)
        return parameters
