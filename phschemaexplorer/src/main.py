import openpyxl
import xlrd
import json
import os
import traceback
from time import perf_counter

__PATH_PREFIX = "PATH_PREFIX"
__HTTP_METHOD = "httpMethod"
__PATH_PARAMETERS = "pathParameters"
__BODY = "body"


def __init_openpyxl(path):
    # return xlrd.open_workbook(path)
    return openpyxl.load_workbook(filename=path, read_only=True, keep_links=False, data_only=True)
    # return openpyxl.load_workbook(path, read_only=True)


def get_excel_data(wb, sheets, out_number):
    def get_sheet(sheet):
        ws = wb[sheet]
        data = []
        count = 0
        rows = ws.iter_rows(min_row=1, max_row=out_number+1)
        for row in rows:
            if count == out_number:
                break
            cells = [str(cell.value) for cell in row]
            none_set = "".join(list(set(cells)))
            data.append((sheet, cells, none_set, len(none_set)))
            count += 1
        return data

    begin = perf_counter()
    data = list(map(get_sheet, sheets))
    wb.close()
    data = list(map(build_data, data))
    end = perf_counter()
    print("iterator {0:.2f}s".format(end - begin))
    begin = end
    return data


def build_data(data):
    def filter_not_title(item):
        count = item[-1]
        is_none_content = item[-2]
        return count > 1 and is_none_content != "None"

    begin = perf_counter()
    content = list(filter(filter_not_title, data))
    read_num = (len(data) - len(content)) + 1
    sheet = content[0][0]
    schema = content[0][1]
    data = list(map(lambda x: x[1], content[1:]))
    end = perf_counter()
    print("build data iterator {0:.2f}s".format(end - begin))
    begin = end
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
        begin = perf_counter()
        wb = __init_openpyxl(path)
        end = perf_counter()
        print("open excel iterator {0:.2f}s".format(end - begin))
        begin = end

        sheets = wb.sheetnames if not body.get("sheet").strip() else [body.get("sheet")]
        out_number = int(body.get("out_number")) if int(body.get("out_number")) > 0 else 20
        return get_excel_data(wb, sheets, out_number)
    except Exception:
        traceback.print_exc()
        return []

