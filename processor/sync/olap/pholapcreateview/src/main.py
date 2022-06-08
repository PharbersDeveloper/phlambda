# import json
import os
from util import *

def lambda_handler(event, context):
    event = json.loads(event["body"])
    response = {
        "status": "",
        "is_exist": False,
    }
    try:
        job_name = event["job_name"]
        ds_name = event["ds_name"]
        tenant_id = event["tenant_id"]
        project_id = event["project_id"]
        table_name = f"{project_id}_{ds_name}"
        view_name = f"{project_id}_{job_name}"
        overwrite = event["overwrite"]
        is_exist = False

        def convert_str2dict(item):
            item["stepId"] = int(item["stepId"])
            item["expressions"] = json.loads(item["expressions"])
            return item

        # DynamoDB查询
        steps = sorted(list(map(convert_str2dict, dynamodb_step_query(view_name))), key=lambda x: x["stepId"])
        db_cols = list(map(lambda item: item["name"], execute_sql(f"desc `{table_name}` FORMAT JSON", tenant_id)["data"]))

        # Filter
        filter_steps = list(filter(lambda item: item["ctype"].startswith("Filter"), steps))
        filter_result = list(map(lambda item: command.get(item["ctype"])(item), filter_steps))

        # cell操作
        cell_operation_steps = list(filter(lambda item: not item["ctype"].startswith("Filter"), steps))
        cell_operation = list(map(lambda item: command.get(item["ctype"])(item, db_cols), cell_operation_steps))

        all_cell_operation = merge_cell_operation(cell_operation)

        sql = build_sql({
            "filter_sql": filter_result,
            "cell_sql": all_cell_operation
        }, table_name)

        print(sql)

        # check view is exist
        result = execute_sql(f"SELECT name FROM system.tables where engine='View' and name = '{view_name}' FORMAT JSON", tenant_id)["data"]
        if result:
            is_exist = True

        # 不存在直接创建
        if not is_exist:
            execute_sql(f"CREATE VIEW `{view_name}` AS {sql} FORMAT JSON", tenant_id)

        # 覆盖
        if overwrite:
            execute_sql(f"DROP VIEW `{view_name}` FORMAT JSON", tenant_id)
            execute_sql(f"CREATE VIEW `{view_name}` AS {sql} FORMAT JSON", tenant_id)

        response["status"] = "succeed"
        response["is_exist"] = is_exist
        response["view_name"] = view_name
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(response, ensure_ascii=False)
        }
    except Exception as e:
        response["status"] = "failed"
        response["error"] = str(e)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(response, ensure_ascii=False)
        }
