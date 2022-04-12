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
import json


class Csv:
    clickhouse = None
    parameters = None
    write_once = None

    def __init__(self):
        # self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        # self.msg_receiver = MsgReceiver()
        # self.logger = PhLogging().phLogger("Excel XLSX TYPE", LOG_DEBUG_LEVEL)
        self.file_name_list = []
        self.schema = None
        self.whileonce = True
        self.clickhouse_client = None
        self.PhS3 = PhS3()
        self.dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1",
                                                aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                                                aws_secret_access_key="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")

    def __create_clickhouse(self, projectId):
        result = self.scanTable({
            "table_name": "resource",
            "limit": 100000,
            "expression": Attr("projectId").eq(projectId),
            "start_key": ""
        })["data"]
        ip = os.environ.get("CLICKHOUSE_HOST")
        if len(result) > 0:
            ip = result[0]["projectIp"]
        self.clickhouse_client = Client(host=ip, port=os.environ.get("CLICKHOUSE_PORT"))

    def parse_data(self, data: list, version):
        print(data)
        # return list(map(lambda x: dict(zip(self.schema+["version"], x)), [i + [version] for i in data]))
        return list(map(lambda x: dict(zip(self.schema, x)),
                        [[str(j) if str(j) != "nan" else "None" for j in i] for i in data]))

    def exists_table(self, table_name):
        clickhouse_tables = [clickhouse_table[0] for clickhouse_table in self.clickhouse_client.execute("show tables")]
        print("exists_table-------------------------------")
        # print(clickhouse_tables)
        if not table_name in clickhouse_tables:
            sql_create_table = self.createClickhouTableSql(table_name)
            print(sql_create_table)
            self.clickhouse_client.execute(sql_create_table)
            print(True)
        print(False)
        # outClickhouse(df, tb, clickhouse_ip, database=db)

    def scanTable(self, data):
        table_name = data["table_name"]
        limit = data["limit"]
        expression = data["expression"]
        start_key = data["start_key"]
        table = self.dynamodb_resource.Table(table_name)
        try:
            if len(start_key) == 0:
                result = table.scan(
                    FilterExpression=expression,
                    Limit=limit,
                )
            else:
                result = table.scan(
                    FilterExpression=expression,
                    Limit=limit,
                    ExclusiveStartKey=start_key
                )
            return {
                "data": result.get("Items"),
                "start_key": result.get("LastEvaluatedKey", "{}")
            }
        except Exception as e:
            print(e)
            return {
                "data": [],
                "start_key": {}
            }

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

    def do_parquet(self, dataf, file_name):
        dataf.columns = self.schema
        dataf.to_parquet(file_name, index=False, partition_cols="version")

    def toclickhouse(self, table_name, data):
        print("to clickhouse -------------------------")
        print(self.schema)
        print(data)
        if len(self.schema) != len(data[0]):
            print("col-----error---------------------")
            return False
        create_sql = self.createClickhouTableSql(table_name)
        print(create_sql)

        self.clickhouse_client.execute(create_sql)
        self.clickhouse_client.execute(f'INSERT INTO {table_name} VALUES', data)
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
            ds_name = parameters.get("ds_name")
            projectId = parameters.get("project_id")
            path = f"/mnt/tmp/{projectId}/tmp/{filename}"
            data_list = pd.read_csv(path, chunksize=10000, header=None)
            table_name = f"{projectId}_{ds_name}"
            skip_first = int(parameters.get("skip_first"))
            skip_next = int(parameters.get("skip_next"))
            print(skip_next)
            print(skip_first)

            self.__create_clickhouse(projectId)
            out_file_name = f"/mnt/tmp/{projectId}/tmp/pharbers/{projectId}/{ds_name}/"
            for i, dataf in enumerate(data_list):
                dataf["version"] = version
                # dataf1 = dataf.drop(labels=skip,axis=0)
                data_l = dataf.values.tolist()
                if self.whileonce:
                    print("not schema insert to clickhouse-------------------")
                    if not skip_first:
                        schemas = [f"col_{count}" if str(col) == "nan" or not col else str(col) for count, col in
                                   enumerate(data_l.pop(0))]
                        self.schema = ["version" if schem == version else schem for schem in schemas]
                    if skip_first:
                        print("will to clickhosue-------------------------------------")
                        data_l = data_l[skip_first:]
                        schemas = [f"col_{count}" if str(col) == "nan" or not col else str(col) for count, col in
                                   enumerate(data_l.pop(0))]
                        self.schema = ["version" if schem == version else schem for schem in schemas]
                        print(self.schema)
                    for i in range(skip_next):
                        data_l.pop(0)
                    parameters["standard_schema"] = [{"src": sch, "des": sch, "type": "String"} for sch in self.schema]
                    self.whileonce = False
                    new_data = self.parse_data(data_l, version)
                    if not self.toclickhouse(table_name, new_data):
                        raise ColumnDuplicate("column duplication")

                self.do_parquet(dataf, out_file_name)

            self.toS3(out_file_name, f"2020-11-11/lake/pharbers/{projectId}/{ds_name}/")
            print("success------------------------------------------------------------------------")
            SaveDataSetCommand(DataSetReceiver()).execute(parameters)  # 建DynamoDB Dataset索引
            SaveDagCommand(DagReceiver()).execute(parameters)
            SaveDagCommand(VersionReceiver()).execute(parameters)

        except ColumnDuplicate as e:
            raise e
        except Exception as e:
            raise Errors(e)
        return parameters