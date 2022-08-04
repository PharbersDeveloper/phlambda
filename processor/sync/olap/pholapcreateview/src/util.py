import decimal
import json
import http.client
import itertools
import boto3
from functools import reduce
from boto3.dynamodb.conditions import Key


def dynamodb_step_query(partition_key):
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return str(o)
            super(DecimalEncoder, self).default(o)
    dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")
    ds_table = dynamodb_resource.Table("step")
    res = ds_table.query(
        KeyConditionExpression=Key("pjName").eq(partition_key)
    )["Items"]
    return json.loads(json.dumps(res, cls=DecimalEncoder, ensure_ascii=False))


def execute_sql(sql, tenant_id):
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(
        Name=tenant_id,
    )
    value = json.loads(response["Parameter"]["Value"])
    conn = http.client.HTTPConnection(host=value["olap"]["PrivateIp"], port="8123")
    # conn = http.client.HTTPConnection(host="127.0.0.1", port="18123")
    headers = {
        'Content-Type': 'text/plain'
    }
    conn.request("POST", "/", sql.encode("utf-8"), headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    if "DB::Exception" in data:
        raise Exception(data)
    return json.loads(data) if len(data) > 0 else {"data": "None"}


def cell_match_mode(match, value):
    cell_match_type = {
        "FULL_STRING": f"'^{value}$'",
        "SUBSTRING": f"'{value}'",
        "PATTERN": f'{value}'
    }
    return cell_match_type[match]


def filter_matching_mode(match, value):
    match_type = {
        "FULL_STRING": f"= '{value}'",
        "SUBSTRING": f"like '%{value}%'",
        "PATTERN": f"'{value}'",
    }
    return match_type[match]


def filter_keep_row(**kwargs):
    exprs = kwargs["exprs"]
    mode = kwargs["mode"]
    return f" {mode} ".join(exprs)


def filter_remove_row(**kwargs):
    exprs = kwargs["exprs"]
    mode = kwargs["mode"]
    return "not(" + f" {mode} ".join(list(map(lambda expr: f"{expr}", exprs))) + ")"


def clear_cell(**kwargs):
    cell_match_type = {
        "FULL_STRING": lambda col, val: f"""if (`{col}` = '{val}', '', `{col}`)""",
        "SUBSTRING": lambda col, val: f"""replaceRegexpAll(`{col}`, '{val}', '')""",
        "PATTERN": lambda col, val: f"""replaceRegexpAll(`{col}`, '{val}', '')""",
    }
    match_mode = kwargs["match_mode"]
    columns = kwargs["columns"]
    values = kwargs["values"]
    result = list(map(lambda col:
                      list(map(lambda value: f"({cell_match_type[match_mode](col, value)} AS `{col}`)",
                               values)), columns))

    return list(reduce(lambda x, y: x + y, result))


def dont_clear_cell(**kwargs):
    cell_match_type = {
        "FULL_STRING": lambda col, val: f"""if (`{col}` != '{val}', '', `{col}`)""",
        "SUBSTRING": lambda col, val: f"""replaceRegexpAll(`{col}`, '[^{val}]', '')""",
        "PATTERN": lambda col, val: f"""replaceRegexpAll(`{col}`, '{val}', '')""",
    }
    match_mode = kwargs["match_mode"]
    columns = kwargs["columns"]
    values = kwargs["values"]
    result = list(map(lambda col:
                      list(map(lambda value: f"({cell_match_type[match_mode](col, value)} AS `{col}`)",
                               values)), columns))
    return list(reduce(lambda x, y: x + y, result))


action_prefix = {
    "KEEP_ROW": "row",
    "REMOVE_ROW": "row",
    "CLEAR_CELL": "cell",
    "DONTCLEAR_CELL": "cell"
}


def filter_action_mode(action):
    action_type = {
        "KEEP_ROW": filter_keep_row,
        "REMOVE_ROW": filter_remove_row,
        "CLEAR_CELL": clear_cell,
        "DONTCLEAR_CELL": dont_clear_cell
    }
    return action_type[action]


def filter_on_value(data):
    values = data["expressions"]["params"]["values"]
    columns = data["expressions"]["params"]["columns"]
    match_mode = data["expressions"]["params"]["matchingMode"]
    action = data["expressions"]["params"]["action"]
    boolean_mode = data["expressions"]["params"]["booleanMode"]

    expr_list = list(map(lambda col:
                         f"""({" OR ".join(list(map(lambda value: f"`{col}` {filter_matching_mode(match_mode, value)}",
                                                    values)))})""", columns))

    return {
        "prefix": action_prefix[action],
        "expr": filter_action_mode(action)(exprs=expr_list, mode=boolean_mode, match_mode=match_mode, columns=columns,
                                           values=values)
    }


def filter_on_number_range(data):
    boolean_mode = data["expressions"]["params"]["booleanMode"]
    action = data["expressions"]["params"]["action"]
    min_value = data["expressions"]["params"]["min"]
    max_value = data["expressions"]["params"]["max"]
    columns = data["expressions"]["params"]["columns"]
    expr_list = list(map(lambda col: f"(`{col}` >= {min_value} AND `{col}` < {max_value})", columns))
    return {
        "prefix": action_prefix[action],
        "expr": filter_action_mode(action)(exprs=expr_list, mode=boolean_mode)
    }


def column_replace(data, cols):
    column = data["expressions"]["params"]["columns"]
    output = data["expressions"]["params"]["output"]
    cols.append(output)
    return {
        "index": data["index"],
        "expr": f"""({f"`{column}`" if column in cols else "' '"} AS `{output}`)"""
    }


def nested_replacement_data(cols, data):
    result = []
    for col in cols:
        replace_list = list(filter(lambda x: x["col"] == col, data))
        if len(replace_list) == 1:
            item = replace_list[0]
            result.append(f"""(replaceRegexpAll(`{item["col"]}`, {item["from"]}, '{item["to"]}') AS `{col}`)""")
        else:
            temp_item = replace_list.pop(0)
            temp_expr_str = f"""replaceRegexpAll(`{temp_item["col"]}`, {temp_item["from"]}, '{temp_item["to"]}')"""
            for item in replace_list:
                temp_expr_str = f"""replaceRegexpAll({temp_expr_str}, {item["from"]}, '{item["to"]}')"""
            result.append(f"""({temp_expr_str} AS `{col}`)""")
    return result


def value_replace(data, cols):
    matching_mode = data["expressions"]["params"]["matchingMode"]
    columns = list(set(data["expressions"]["params"]["columns"]))
    mapping = list(map(lambda item: {"from": cell_match_mode(matching_mode, item["from"]), "to": item["to"]},
                       data["expressions"]["params"]["mapping"]))
    cols_map = list(map(lambda col: {"col": col}, columns))
    value_replace_mapping = list(
        map(lambda item: reduce(lambda x, y: dict(x, **y), item), itertools.product(mapping, cols_map)))
    expr = ", ".join(nested_replacement_data(columns, value_replace_mapping))
    return {
        "index": data["index"],
        "expr": expr
    }


def fill_empty_with_value(data, cols):
    columns = list(set(data["expressions"]["params"]["columns"]))
    value = data["expressions"]["params"]["value"]
    if len(value) > 100:
        raise Exception("length is greater than 100 `value`")
    if len(value) == 0 or " " in value:
        raise Exception("cannot be empty `value`")
    expr = ", ".join(list(map(lambda col: f"""(multiIf(`{col}` == '', '{value}', `{col}`)) AS `{col}`)""", columns)))
    return {
        "index": data["index"],
        "expr": expr
    }


def merge_cell_operation(data):
    result = sorted(data, key=lambda x: x["index"])
    return result


def build_sql(data, table):
    filter_sql = data["filter_sql"]
    cell_sql = data["cell_sql"]
    temp_sql_str = f"select *, 1 AS __match from `{table}`"

    if cell_sql:
        temp_item = cell_sql.pop(0)
        temp_sql_str = f"""select *, {temp_item["expr"]} from ({temp_sql_str})"""
        for item in cell_sql:
            temp_sql_str = f"""select *, {item["expr"]} from ({temp_sql_str})"""

    filter_cell = list(filter(lambda item: item["prefix"] == "cell", filter_sql))
    filter_row = list(filter(lambda item: item["prefix"] == "row", filter_sql))

    if filter_cell:
        for item in filter_cell:
            for expr in item["expr"]:
                temp_sql_str = f"""select *, {expr} from ({temp_sql_str})"""

    if filter_row:
        row_cond = " AND ".join(list(map(lambda item: item["expr"], filter_row)))
        temp_sql_str = f"""select * from (select *, {row_cond} AS __match from ({temp_sql_str}))"""

    return f"select * from ({temp_sql_str})"


command = {
    "FilterOnValue": filter_on_value,
    "FilterOnNumericalRange": filter_on_number_range,
    "ColumnReplace": column_replace,
    "ReplaceValue": value_replace,
    "FillEmptyWithValue": fill_empty_with_value,
}
