import json
import http.client
import urllib.parse


def executeSql(sql, method):
    conn = http.client.HTTPConnection(host="192.168.16.117", port="8123")
    url = urllib.parse.quote("/ch/?query=" + sql, safe=":/?=&")
    conn.request(method, url)
    res = conn.getresponse()
    return res.read().decode("utf-8")


def lambda_handler(event, context):
    # 直接转proxy转发
    args = eval(event["body"])
    res = executeSql(args["query"], "GET")

    print(res)
    rows = filter(lambda x: x != '', res.split("\n"))

    # 这里没有任何的错误处理
    columns = args["schema"]

    final_res = []
    for row in rows:
        cells = row.split("\t")

        tmp = {}
        for cell in cells:
            index = cells.index(cell)
            tmp[columns[index]] = cell

        final_res.append(tmp)

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(final_res, ensure_ascii=False)
    }
