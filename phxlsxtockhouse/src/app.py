# /usr/local/bin/python3

import os
import re
import json
from src.execl import Excel
from clickhouse_driver import Client

# 这个是环境变量参数
# g_batch_size = 5
# 这个是一个参数从外边传进来
# file_name = "/Users/qianpeng/Desktop/MAPPING_to QLX.xlsx"
# sheet_name = "Sheet1"
# mapper = [{"src": "通用名称", "des": "通用名称", "type": "String"}, {"src": "商品名称", "des": "商品名称", "type": "String"},
#           {"src": "生产企业", "des": "生产企业", "type": "String"}, {"src": "剂型", "des": "剂型", "type": "String"},
#           {"src": "规格", "des": "规格", "type": "String"}, {"src": "包装数量", "des": "包装数量", "type": "Int32"},
#           {"src": "包装单位", "des": "包装单位", "type": "String"}, {"src": "PACKCODE", "des": "packcode", "type": "String"},
#           {"src": "项目", "des": "项目", "type": "String"}]
# title_row = 3
# skip_next = 3
# des_table_name = "prod" + sheet_name
#
# fields = ", ".join(list(map(lambda item: "`{0}` {1}".format(item["des"], item["type"]), mapper)))
#
# # 创建表
# create_table = "CREATE TABLE IF NOT EXISTS {0}.{1} ({2}) ENGINE=TinyLog".format("default", des_table_name, fields)
# client.execute(create_table)
# print(create_table)

__BATCH_SIZE = "BATCH_SIZE"
__CLICKHOUSE_HOST = "CLICKHOUSE_HOST"
__CLICKHOUSE_PORT = "CLICKHOUSE_PORT"
__CLICKHOUSE_DB = "CLICKHOUSE_DB"
__FILE_PATH = "PATH_PREFIX"


def lambda_handler(event, context):
    body = json.loads(event["body"])
    file_name = body["file_name"]
    sheet_name = body["sheet_name"]
    mapper = body["mapper"]
    title_row = body["skip_first"]
    skip_next = body["skip_next"]
    version = body["version"]
    des_table_name = file_name.split(".")[0] + sheet_name
    des_table_name = re.sub("[\n\t\s_（） ， +()-./\"]", "", des_table_name)

    zipMapper = mapper +\
                [{"src": "version", "des": "version", "type": "String"}]

    fields = list(map(lambda item: "`{0}` {1}".format(item["des"], item["type"]), zipMapper))

    client = Client(host=os.environ.get(__CLICKHOUSE_HOST), port=os.environ.get(__CLICKHOUSE_PORT))

    # 创建表
    create_table = "CREATE TABLE IF NOT EXISTS {0}.{1} ({2}) ENGINE=TinyLog" \
        .format(os.environ.get(__CLICKHOUSE_DB), des_table_name, ", ".join(fields))
    print(create_table)
    client.execute(create_table)


    def call_back(data, adapted_mapper):
        cols_description = list(map(lambda col: "`{0}`".format(col['des']), adapted_mapper))
        cols_description.append("`version`")
        cols_description = ",".join(cols_description)
        sql = 'INSERT INTO ' + des_table_name + ' (' + cols_description + ') ' + 'VALUES'

        def add_col(item):
            item["version"] = version
            return item
        excel_data = list(map(add_col, data))
        client.execute(sql, excel_data)

    excel = Excel("{0}{1}".format(os.environ.get(__FILE_PATH), file_name),
                  sheet_name, title_row, skip_next, mapper,
                  int(os.environ.get(__BATCH_SIZE)))
    excel.batchReader(call_back)
    return {}
