import openpyxl
import json
import os
import traceback

__PATH_PREFIX = "PATH_PREFIX"
__HTTP_METHOD = "httpMethod"
__PATH_PARAMETERS = "pathParameters"
__BODY = "body"


def __init_openpyxl(path):
    return openpyxl.load_workbook(path, read_only=True)


def get_excel_data(wb, sheets, out_number):
    def get_sheet(sheet):
        ws = wb[sheet]
        data = []
        count = 0
        for row in ws.rows:
            if count == out_number:
                break
            cells = [str(cell.value) for cell in row]
            none_set = "".join(list(set(cells)))
            data.append((sheet, cells, none_set, len(none_set)))
            count += 1
        return data
    data = list(map(get_sheet, sheets))
    wb.close()
    data = list(map(build_data, data))
    return data


def build_data(data):
    def filter_not_title(item):
        count = item[-1]
        is_none_content = item[-2]
        return count > 1 and is_none_content != "None"

    content = list(filter(filter_not_title, data))
    read_num = (len(data) - len(content)) + 1
    sheet = content[0][0]
    schema = content[0][1]
    data = list(map(lambda x: x[1], content[1:]))
    return {
        "readNumber": read_num,
        "sheet": sheet,
        "schema": schema,
        "data": data
    }


def lambda_handler(event, context):
    try:
        body = event
        original_file = body.get("original_file")
        path = os.environ.get(__PATH_PREFIX) + body.get("tempfile")
        wb = __init_openpyxl(path)
        sheets = wb.sheetnames if not body.get("sheet").strip() else [body.get("sheet")]
        out_number = int(body.get("out_number")) if int(body.get("out_number")) > 0 else 20
        return get_excel_data(wb, sheets, out_number)
    except Exception:
        traceback.print_exc()
        return []


if __name__ == '__main__':
    os.environ[__PATH_PREFIX] = "/Users/qianpeng/Desktop/"
    event = open("../../events/ph-schema-explorer/event_find.json", 'r+').read()
    result = lambda_handler(json.loads(event), None)
    print(result)
