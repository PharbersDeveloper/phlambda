import json
import http.client
import urllib.parse
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Attr
from phprojectargs.projectArgs import ProjectArgs


def executeSql(sql, method, projectId):
    dynamodb = DynamoDB()
    args = ProjectArgs(projectId)
    proxies = args.get_proxy_list()

    # result = dynamodb.scanTable({
    #     "table_name": "resource",
    #     "limit": 100000,
    #     "expression": Attr("projectId").eq(projectId),
    #     "start_key": ""
    # })["data"]

    ip = "192.168.16.117"
    if len(proxies) > 0:
        ip = proxies[0]

    conn = http.client.HTTPConnection(host=ip, port="8123")
    url = urllib.parse.quote("/ch/?query=" + sql, safe=":/?=&")
    conn.request(method, url)
    res = conn.getresponse()
    return res.read().decode("utf-8")


def lambda_handler(event, context):
    try:
        # 直接转proxy转发
        args = eval(event["body"])
        res = executeSql(args["query"], "GET", args["projectId"])

        rows = list(filter(lambda x: x != '', res.split("\n")))

        if len(rows) == 1 and "UNKNOWN_TABLE" in "".join(rows):
            raise Exception("UNKNOWN_TABLE")

        # 这里没有任何的错误处理
        columns = args["schema"]

        final_res = []
        for row in rows:
            cells = row.split("\t")

            tmp = {}
            for index in range(len(cells)):
                tmp[columns[index]] = cells[index]

            final_res.append(tmp)
            
        print(final_res)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(final_res, ensure_ascii=False)
        }
    except Exception as e:
        print("Error =>  \n")
        print(e)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "status": "failed",
                "code": 500,
                "message": str(e)
            }, ensure_ascii=False)
        }
