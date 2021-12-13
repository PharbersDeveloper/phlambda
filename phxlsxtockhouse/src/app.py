# /usr/local/bin/python3
import re
import os
import json
import time
from util.execl import Excel
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Attr
from util.ClieckHouse import ClickHouse

__BATCH_SIZE = "BATCH_SIZE"
# __CLICKHOUSE_HOST = "CLICKHOUSE_HOST"
# __CLICKHOUSE_PORT = "CLICKHOUSE_PORT"
__CLICKHOUSE_DB = "CLICKHOUSE_DB"
__FILE_PATH = "PATH_PREFIX"
__TYPE_STRUCTURE = {
    "String": str
}
client = ClickHouse(host="192.168.16.117", port="9000").getClient()
reg = "[\n\t\s（），+()-./\"'\\\\]"


def executeChDriverSql(sql):
    result = client.execute(sql)
    print(result)
    return result


def insertData(sql, values):
    return client.execute(sql, values)


def updateAction(item, dynamodb, state):
    item["jobDesc"] = state
    dynamodb.putData({
        "table_name": "action",
        "item": item
    })


def insetNotification(item, dynamodb, data, state, error):
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
    # label = message.get("label", "[]")
    version = message.get("version", "0.0.0")
    des_table_name = message["destination"]
    print("message =====> \n")
    print(message)
    mapper = message.get("mapper", getExcelMapper(file_name, sheet_name, title_row + 1))
    converted_mapper = list(map(lambda item: {
        "src": re.sub(reg, "_", item["src"]),
        "des": re.sub(reg, "_", item["des"]),
        "type": item["type"]
    }, mapper)) + [{"src": "version", "des": "version", "type": "String"}]
    print("Mapper   =>>>> \n")
    print(converted_mapper)

    result = dynamodb.scanTable({
        "table_name": "dataset",
        "limit": 100000,
        "expression": Attr("name").eq(des_table_name) & Attr("projectId").eq(item["projectId"]),
        "start_key": ""
    })
    print("Alex DynamoDB =>>>>>> \n")
    print(result)
    data = result["data"]
    if len(data) > 0:
        schema = set(map(lambda key: key["des"], json.loads(data[0]["schema"])))
        fileSchema = set(map(lambda key: key["des"], converted_mapper))
        if len(schema - fileSchema) != 0:
            raise Exception("Schema Not Matched,请使用高级映射！")
    dsId = data[0]["id"] if len(data) > 0 else file_name
    label = data[0]["label"] if len(data) > 0 else "[]"
    dynamodb.putData({
        "table_name": "dataset",
        "item": {
            "id": dsId,
            "projectId": item["projectId"],
            "date": int(round(time.time() * 1000)),
            "name": des_table_name,
            "schema": json.dumps(converted_mapper, ensure_ascii=False),
            "label": label,
            "version": version
        }
    })
    write2Clickhouse(message, mapper, item, dynamodb)


def insertDag(item, dynamodb):
    message = json.loads(item["message"])
    des_table_name = message["destination"]
    file_name = message["fileId"]
    result = dynamodb.scanTable({
        "table_name": "dataset",
        "limit": 100000,
        "expression": Attr("name").eq(des_table_name) & Attr("projectId").eq(item["projectId"]),
        "start_key": ""
    })
    print("Alex DynamoDB DAG =>>>>>> \n")
    print(result)
    data = result["data"]
    dsId = data[0]["id"] if len(data) > 0 else file_name
    dynamodb.putData({
        "table_name": "dag",
        "item": {
            "id": "",
            "projectId": item["projectId"],
            "sortVersion": f"developer_{dsId}",
            "cat": "dataset",
            "cmessage": "",
            "ctype": "node",
            "flowVersion": "developer",
            "level": "-99999",
            "name": des_table_name,
            "position": """{"x": "0", "y": "0", "z": "0", "w": "0", "h": "0"}""",
            "representId": dsId,
            "runtime": "uploaded"
        }
    })

    pass


def getExcelMapper(file_name, sheet_name, skip_first):
    result = Excel.getSchema(os.environ.get(__FILE_PATH) + file_name, sheet_name, skip_first)
    return list(map(lambda item: {"src": item, "des": item, "type": "String"}, result))


def write2Clickhouse(message, mapper, item, dynamodb):
    print("Alex =====> write2Clickhouse \n")
    title_row = message["skipValue"]
    skip_next = message["jumpValue"]
    version = message.get("version", "0.0.0")
    file_name = message["fileId"]
    sheet_name = message["fileSheet"]
    des_table_name = message["destination"]
    tableName = item["projectId"] + "_" + des_table_name
    zipMapper = mapper + [{"src": "version", "des": "version", "type": "String"}]
    fields = ", ".join(
        list(map(lambda item: "`{0}` {1}".format(re.sub(reg, "_", item['des']), item["type"]), zipMapper)))

    print("fields ====> \n")
    print(fields)

    # 创建表
    create_table = f"CREATE TABLE IF NOT EXISTS " \
                   f"{os.environ.get(__CLICKHOUSE_DB)}.`{tableName}` " \
                   f"({fields}) ENGINE=MergeTree() PRIMARY KEY version"
    print(create_table)
    result = executeChDriverSql(create_table)
    print("Create Table ========> \n")
    print(result)

    countSql = f"SELECT COUNT(1) FROM " \
               f"{os.environ.get(__CLICKHOUSE_DB)}.`{tableName}` " \
               f"WHERE version = '{version}'"
    print("count sql ======> \n")
    print(countSql)
    count = list(executeChDriverSql(countSql).pop()).pop()
    if count > 0:
        raise Exception("version already exist")

    # excel回调数据
    def callBack(data, adapted_mapper, batch_size, hit_count):
        print("data ===> \n")
        print(data)
        cols_description = list(map(lambda col: "`{0}`".format(re.sub(reg, "_", col['des'])), adapted_mapper))
        cols_description.append("`version`")
        cols_description = ",".join(cols_description)
        sql = f"INSERT INTO {os.environ.get(__CLICKHOUSE_DB)}.`{tableName}` ({cols_description}) VALUES"

        def add_col(item):
            value = {}
            for x in list(item.keys()):
                mi = list(filter(lambda mapperItem: mapperItem["des"] == x, mapper))[0]
                fieldType = __TYPE_STRUCTURE[mi["type"]]
                value[re.sub(reg, "_", x)] = re.sub("[']", "", fieldType(item[x]))
            value["version"] = version
            return value

        print("sql ====> \n")
        print(sql)
        execl_data = list(map(add_col, data))
        insertData(sql, execl_data)

        hit_value = 100 / batch_size
        progress = round(float(hit_count * hit_value), 2)
        print("==========> {} \n".format(progress))
        insetNotification(item, dynamodb, {"progress": progress}, "succeed" if progress >= 100 else "running", "")

    excel = Excel("{0}{1}".format(os.environ.get(__FILE_PATH), file_name),
                  sheet_name, title_row + 1, skip_next, mapper,
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
            print("Alex 进入  =====> \n")
            print(record["eventName"].lower())
            print(new_image)
            print(new_image.get("jobCat", {"S": "None"})["S"])
            if record["eventName"].lower() == "insert" and new_image.get("jobCat", {"S": "None"})["S"] == "project_file_to_DS":
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
                    insertDag(item, dynamodb)
                    updateAction(item, dynamodb, "created")

    except Exception as e:
        print("error: \n")
        print(str(e))
        print(history)
        updateAction(history, dynamodb, "failed")
        insetNotification(history, dynamodb, {"progress": -1}, "failed", str(e))
