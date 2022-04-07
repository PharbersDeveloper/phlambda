
import constants.DefinValue as DV
from handler.Command.DagReceiver import DagReceiver
from handler.Command.DataSetReceiver import DataSetReceiver
from handler.Command.SaveCommand import SaveDataSetCommand, SaveDagCommand

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
        self.clickhouse_client = None
        self.dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1",
                                                aws_access_key_id="AKIAWPBDTVEANKEW2XNC",
                                                aws_secret_access_key="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")

    def __create_clickhouse(self, projectId):
        result = self.scanTable({
            "table_name": "resource",
            "limit": 100000,
            "expression": Attr("projectId").eq("ggjpDje0HUC2JW"),
            "start_key": ""
        })["data"]
        ip = os.environ.get("CLICKHOUSE_HOST")
        if len(result) > 0:
            ip = result[0]["projectIp"]
        self.clickhouse_client = Client(host=ip, port=os.environ.get("CLICKHOUSE_PORT"))

    def parse_data(self, data: list, version):
        print(data)
        # return list(map(lambda x: dict(zip(self.schema+["version"], x)), [i + [version] for i in data]))
        return list(map(lambda x: dict(zip(self.schema + ["version"], x)),
                        [[str(j) if str(j) != "nan" else "None" for j in i + [version]] for i in data]))

    def exists_table(self, table_name):
        clickhouse_tables = [clickhouse_table[0] for clickhouse_table in self.clickhouse_client.execute("show tables")]
        print("exists_table-------------------------------")
        print(clickhouse_tables)
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
        def getSchemeSql():
            sql_scheme = ""
            new_schema = self.schema + ["version"]
            for i in new_schema:
                sql_scheme += f"`{i}` String,"
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
        print("to clickhouse -------------------------")
        print(data)
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
            "jobCat": "project_file_to_DS_",
        }



        version = parameters.get("version")
        filename = parameters.get("file_name")
        ds_name = parameters.get("ds_name")
        projectId = parameters.get("project_id")
        path = f"/Users/moke/worker_space/phlambda/phxlsxtockhouse/src/handler/Strategy/{filename}"
        path = f"/mnt/tmp/{projectId}/tmp/{filename}"
        data_list = pd.read_csv(path, chunksize=10)
        table_name = f"{projectId}_{ds_name}"

        # ds_name = "test2222222222"
        # version = data.get("version")
        # file_name = data.get("file_name")
        # temp_file = data.get("path")
        # projectId = data.get("projectId")
        # data_list = pd.read_csv(temp_file, chunksize=10)
        # table_name = f"{projectId}_{ds_name}"

        self.__create_clickhouse(projectId)

        for i, dataf in enumerate(data_list):
            data_l = dataf.values.tolist()
            if not self.schema:
                print("not schema insert to clickhouse-------------------")
                self.schema = dataf.columns.values.tolist()
                new_data = self.parse_data(data_l, version)
                self.toclickhouse(table_name, new_data)
            out_file_name = f"/mnt/tmp/{projectId}/tmp/" + filename.split(".")[0] + "_" + str(i + 1) + ".parquet"
            # out_file_name = f"/Users/moke/worker_space/phlambda/phxlsxtockhouse/src/handler/Strategy/parquet/" + filename + "_" + str(i + 1) + ".parquet"
            self.do_parquet(dataf, out_file_name)
            self.file_name_list.append(out_file_name)

        self.toS3()
        print("success------------------------------------------------------------------------")
        # SaveDataSetCommand(DataSetReceiver()).execute(parameters)  # 建DynamoDB Dataset索引
        # SaveDagCommand(DagReceiver()).execute(parameters)  # 写Dag
