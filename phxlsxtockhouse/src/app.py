# /usr/local/bin/python3

import os
import json
import time
import http.client
import urllib.parse
from util.execl import Excel
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Key, Attr
from util.GenerateID import GenerateID

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
    print(url)
    conn.request(type, url)
    res = conn.getresponse()
    return res.read().decode("utf-8")


def updateAction(item, dynamodb, state):
    item["jobDesc"] = state
    dynamodb.putData({
        "table_name": "action",
        "item": item
    })


def insterNotification(item, dynamodb, data, state, error):
    print("Alex Notification =>>>>>> \n")
    print(item)
    message = json.loads(item["message"])
    # TODO： 硬code + 无防御，有机会重构
    dynamodb.putData({
        "table_name": "notification",
        "item": {
            "id": item["id"],
            "projectId": item["projectId"],
            "code": 0,
            "comments": "",
            "date": int(round(time.time() * 1000)),
            "jobCat": "notification",
            "jobDesc": state,
            "message": json.dumps({
                "type": "operation",
                "opname": item["owner"],
                "opgroup": message.get("opgroup", "0"),
                "cnotification": {
                    "status": "project_file_to_DS_{}".format(state),
                    "data": json.dumps(data),
                    "error": error
                }
            }),
            "owner": item["owner"],
            "showName": item["showName"]
        }
    })

def insertDataset(item, dynamodb):
    message = json.loads(item["message"])
    title_row = message["skipValue"]
    file_name = message["fileId"]
    sheet_name = message["fileSheet"]
    label = message.get("label", "[]")
    version = message.get("version", "0.0.0")
    des_table_name = message["destination"]
    if title_row == 0:
        title_row += 1
    else:
        title_row += 2
    mapper = message.get("mapper", getExcelMapper(file_name, sheet_name, title_row))
    print(mapper)

    result = dynamodb.scanTable({
        "table_name": "dataset",
        "limit": 100000,
        "expression": Attr("name").eq(des_table_name),
        "start_key": ""
    })
    print("Alex DynamoDB =>>>>>> \n")
    print(result)

    dynamodb.putData({
        "table_name": "dataset",
        "item": {
            "id": result["data"][0]["id"] if len(result["data"]) > 0 else file_name,
            "projectId":  result["data"][0]["projectId"] if len(result["data"]) > 0 else item["projectId"],
            "date": int(round(time.time() * 1000)),
            "name": des_table_name,
            "schema": json.dumps(mapper, ensure_ascii=False),
            "label": label,
            "version": version
        }
    })
    write2Clickhouse(message, mapper, item, dynamodb)


def getExcelMapper(file_name, sheet_name, skip_first):
    result = Excel.getSchema(os.environ.get(__FILE_PATH) + file_name, sheet_name, skip_first)
    return list(map(lambda item: {"src": item, "des": item, "type": "String"}, result))


def write2Clickhouse(message, mapper, item, dynamodb):
    title_row = message["skipValue"]
    skip_next = message["jumpValue"]
    version = message.get("version", "0.0.0")
    file_name = message["fileId"]
    sheet_name = message["fileSheet"]
    des_table_name = message["destination"]
    zipMapper = mapper + [{"src": "version", "des": "version", "type": "String"}]

    fields = ", ".join(list(map(lambda item: "`{0}` {1}".format(item["des"], item["type"]), zipMapper)))

    if title_row == 0:
        title_row += 1
    else:
        title_row += 2

    # 创建表
    create_table = "CREATE TABLE IF NOT EXISTS {0}.`{1}` ({2}) ENGINE=MergeTree() PRIMARY KEY version" \
        .format(os.environ.get(__CLICKHOUSE_DB), des_table_name, fields)
    print(create_table)
    result = executeSql(create_table, "POST")
    print("Create Table ========> \n")
    print(result)

    res = executeSql("select count(1) from `{0}` where version = '{1}'".format(des_table_name, version), "POST")
    if int(res.replace("\n", "")) > 0:
        raise Exception("version already exist")

    # excel回调数据
    def callBack(data, adapted_mapper, batch_size, hit_count):
        cols_description = list(map(lambda col: "`{0}`".format(col['des']), adapted_mapper))
        cols_description.append("`version`")
        cols_description = ",".join(cols_description)
        sql = 'INSERT INTO `' + des_table_name + '` (' + cols_description + ') ' + 'VALUES'

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

        hit_value = 100 / batch_size
        progress = round(float(hit_count * hit_value), 2)
        print("==========> {} \n".format(progress))
        insterNotification(item, dynamodb, {"progress": progress}, "succeed" if progress >= 100 else "running", "")

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
        insterNotification(history, dynamodb, {"progress": -1}, "failed", str(e))
    return {}
