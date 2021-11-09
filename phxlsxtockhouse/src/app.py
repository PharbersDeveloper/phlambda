# /usr/local/bin/python3

import os
import json
import time
import http.client
import urllib.parse
from util.execl import Excel
from util.AWS.DynamoDB import DynamoDB

__BATCH_SIZE = "BATCH_SIZE"
# __CLICKHOUSE_HOST = "CLICKHOUSE_HOST"
# __CLICKHOUSE_PORT = "CLICKHOUSE_PORT"
__CLICKHOUSE_DB = "CLICKHOUSE_DB"
__FILE_PATH = "PATH_PREFIX"
__TYPE_STRUCTURE = {
    "String": str
}


def executeSql(sql, type):

    conn = http.client.HTTPConnection(host="192.168.16.117", port="8123")
    url = urllib.parse.quote("/ch/?query=" + sql, safe=':/?=&')
    conn.request(type, url)
    res = conn.getresponse()
    return res.read().decode("utf-8")


def updateAction(item, dynamodb, state):
    item["jobDesc"] = state
    dynamodb.putData({
        "table_name": "action",
        "item": item
    })


def insertDataset(item, dynamodb):
    message = json.loads(item["message"])
    title_row = message["skipValue"]
    file_name = message["fileId"]
    sheet_name = message["fileSheet"]
    label = message.get("label", "[]")
    version = message.get("version", "0.0.0")
    des_table_name = message["destination"]
    mapper = message.get("mapper", getExcelMapper(file_name, sheet_name, title_row))
    dynamodb.putData({
        "table_name": "dataset",
        "item": {
            "id": file_name,
            "projectId": item["projectId"],
            "date": int(round(time.time() * 1000)),
            "name": des_table_name,
            "schema": json.dumps(mapper, ensure_ascii=False),
            "label": label,
            "version": version
        }
    })
    write2Clickhouse(message, mapper)


def getExcelMapper(file_name, sheet_name, skip_first, skip_next=0):
    result = Excel.getSchema(os.environ.get(__FILE_PATH) + file_name, sheet_name, skip_first, skip_next)
    return list(map(lambda item: {"src": item, "des": item, "type": "String"}, result))


def write2Clickhouse(message, mapper):
    title_row = message["skipValue"]
    skip_next = message["jumpValue"]
    version = message.get("version", "0.0.0")
    file_name = message["fileId"]
    sheet_name = message["fileSheet"]
    des_table_name = message["destination"]
    zipMapper = mapper + [{"src": "version", "des": "version", "type": "String"}]

    fields = ", ".join(list(map(lambda item: "`{0}` {1}".format(item["des"], item["type"]), zipMapper)))

    # 创建表
    create_table = "CREATE TABLE IF NOT EXISTS {0}.{1} ({2}) ENGINE=MergeTree() PRIMARY KEY version" \
        .format(os.environ.get(__CLICKHOUSE_DB), des_table_name, fields)
    print(create_table)
    executeSql(create_table, "POST")

    res = executeSql("select count(1) from {0} where version = '{1}'".format(des_table_name, version), "POST")
    if int(res.replace("\n", "")) > 0:
        raise Exception("version already exist")

    # excel回调数据
    def callBack(data, adapted_mapper):
        cols_description = list(map(lambda col: "`{0}`".format(col['des']), adapted_mapper))
        cols_description.append("`version`")
        cols_description = ",".join(cols_description)
        sql = 'INSERT INTO ' + des_table_name + ' (' + cols_description + ') ' + 'VALUES'

        def add_col(item):
            for x in list(item.keys()):
                mi = list(filter(lambda mapperItem: mapperItem["des"] == x, mapper))[0]
                fieldType = __TYPE_STRUCTURE[mi["type"]]
                item[x] = fieldType(item[x])
            item["version"] = version
            values = list(map(lambda v: "'{0}'".format(v), list(item.values())))
            return "(" + ",".join(values) + ")"

        excel_data = ",".join(list(map(add_col, data)))
        sql = sql + " " + excel_data + ";"
        print(sql)
        executeSql(sql, "POST")

    excel = Excel("{0}{1}".format(os.environ.get(__FILE_PATH), file_name),
                  sheet_name, title_row, skip_next, mapper,
                  int(os.environ.get(__BATCH_SIZE)))
    excel.batchReader(callBack)


def lambda_handler(event, context):
    records = event["Records"]
    dynamodb = DynamoDB()
    # import base64
    # from util.AWS.STS import STS
    # from constants.Common import Common

    # sts = STS().assume_role(
    #     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
    #     "Ph-Back-RW"
    # )
    # dynamodb = DynamoDB(sts=sts)
    history = {}
    try:
        data = []
        for record in records:
            if record["eventName"].lower() != "insert":
                continue

            new_image = record["dynamodb"]["NewImage"]
            if record["eventName"].lower() == "insert" and new_image["jobCat"]["S"] == "project_file_to_DS":
                item = {}
                for field in list(new_image.keys()):
                    value = new_image[field]
                    v_k = list(value.keys())[0]
                    item[field] = value[v_k]
                data.append(item)

                for item in data:
                    print(item)
                    history = item
                    insertDataset(item, dynamodb)
                    updateAction(item, dynamodb, "created")

    except Exception as e:
        print("error: \n")
        print(e)
        updateAction(history, dynamodb, "failed")
    return {}
