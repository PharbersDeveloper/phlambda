import time

import pandas as pd
import boto3
import os


# def do_parquet(fin_list, file_name, schema):
#     dataf = pd.DataFrame(fin_list)
#     dataf.columns = schema
#     dataf.to_parquet(file_name, index=False)
#
# count = 0
# outcount = 100
# temp_file = "test2.csv"
#
#
# # while True:
# #     data = pd.read_csv(temp_file, skiprows=count, nrows=outcount, encoding="utf-8")
# #     body = data.values.tolist()
# #     print(body)
# #     count += outcount
# #     if not body:
# #         break
# temp_file = "test1.csv"
# data = pd.read_csv(temp_file, chunksize=10)
# for i in data:
#     print(i)
# # print(data.columns.values.tolist())
# # print(i.values.tolist())
# # print(i.columns.values.tolist())
#
# a = [i+["111111111"] for i in data.__next__().values.tolist()]
# print(a)


# from constants.Errors import Errors, FileNotFound, NotXlsxFile, SchemaNotMatched, VersionAlreadyExist, ColumnDuplicate
# from handler.Strategy.Strategy import Strategy
# from openpyxl.utils.exceptions import InvalidFileException

from handler.Command.WriteReceiver import WriteReceiver
from handler.Command.WriteS3Command import WriteS3Command
# from handler.Command.CheckSchemaReceiver import CheckSchemaReceiver
# from handler.Command.CheckCommand import CheckSchemaConsistencyCommand
# from handler.Command.DagReceiver import DagReceiver
# from handler.Command.DataSetReceiver import DataSetReceiver
# from handler.Command.SaveCommand import SaveDataSetCommand, SaveDagCommand
# from handler.Command.MsgReceiver import MsgReceiver
# from handler.Command.SendMsgCommand import SendMsgRunCommand
# from handler.Command.UploadS3Command import UploadS3Command
# from handler.Command.RemovePathCommand import RemovePathCommand
from boto3.dynamodb.conditions import Attr
# from util.execl import Excel
from util.log.phLogging import PhLogging, LOG_DEBUG_LEVEL
import numpy as np
import os
import re
from clickhouse_driver import Client
import json
import constants.DefinValue as DV
# import constants.Common as Common


class Csv:
    clickhouse = None
    parameters = None
    write_once = None

    def __init__(self):
        # self.dynamodb = Common.EXTERNAL_SERVICES["dynamodb"]
        # self.msg_receiver = MsgReceiver()
        self.logger = PhLogging().phLogger("Excel XLSX TYPE", LOG_DEBUG_LEVEL)
        self.file_name_list = []
        self.schema = None
        self.clickhouse_client = None

    def __create_clickhouse(self, projectId):
        dynamodb = boto3.client("dynamodb", region_name="cn-northwest-1",
                                       aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                                       aws_secret_access_key="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")
        result = dynamodb.scanTable({
            "table_name": "resource",
            "limit": 100000,
            "expression": Attr("projectId").eq(projectId),
            "start_key": ""
        })["data"]
        ip = os.environ[DV.CLICKHOUSE_HOST]
        if len(result) > 0:
            ip = result[0]["projectIp"]
        self.clickhouse_client = Client(host=ip, port=os.environ[DV.CLICKHOUSE_PORT])

    def parse_data(self, data: list, version):
        print(data)
        return list(map(lambda x: dict(zip(self.schema+["version"], x)), [i + [version] for i in data]))

    def exists_table(self, table_name):
        clickhouse_tables = [clickhouse_table[0] for clickhouse_table in self.clickhouse_client.execute("show tables")]
        if not table_name in clickhouse_tables:
            sql_create_table = self.createClickhouTableSql(table_name)
            self.clickhouse_client.execute(sql_create_table)
            print(True)
        print(False)
        # outClickhouse(df, tb, clickhouse_ip, database=db)

    def createClickhouTableSql(self, table_name, database='default', order_by='', partition_by='version'):
        def getSchemeSql():
            sql_scheme = ""
            for i in self.schema:
                sql_scheme += f"`{i}` 'String',"
            sql_scheme = re.sub(r",$", "", sql_scheme)
            return sql_scheme
        return f"CREATE TABLE IF NOT EXISTS {database}.{table_name}({getSchemeSql()}) ENGINE = MergeTree() ORDER BY tuple({order_by}) PARTITION BY {partition_by};"

    def toS3(self):
        s3 = boto3.resource('s3')
        for i in self.file_name_list:
            s3.meta.client.upload_file(i, 'ph-platform', f'2020-11-11/download/parquet/{i.split("/")[-1]}')
            os.remove(i)

    def do_parquet(self, dataf, file_name):
        # dataf = pd.DataFrame(data_list)
        dataf.columns = self.schema
        dataf.to_parquet(file_name, index=False)

    def toclickhouse(self, table_name, data):
        self.exists_table(table_name)
        self.createClickhouTableSql(table_name)
        self.clickhouse_client.execute(f'INSERT INTO {table_name} VALUES', data)

    def do_exec(self, data):

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
            "jobCat": "project_file_to_DS_"
        }

        version = parameters.get("version")
        table_name = parameters.get("file_name")
        temp_file = parameters.get("path")
        data_list = pd.read_csv(temp_file, chunksize=10)

        for i, dataf in enumerate(data_list):
            data_l = dataf.values.tolist()
            if not self.schema:
                self.schema = dataf.columns.values.tolist()
                new_data = self.parse_data(data_l, version)
                self.toclickhouse(table_name, new_data)
            out_file_name = "parquet/" + table_name+"_"+str(i+1)+".parquet"
            self.do_parquet(dataf, out_file_name)
            self.file_name_list.append(out_file_name)

        self.toS3()

data = {"version": "1", "table_name": "test1", "temp_file": "test1.csv"}
csv = Csv().do_exec(data)
