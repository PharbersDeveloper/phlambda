import json
import http.client
import urllib.parse
import boto3
from util.AWS.DynamoDB import DynamoDB
from boto3.dynamodb.conditions import Attr
# from phprojectargs.projectArgs import ProjectArgs

ssm = boto3.client('ssm')

def executeSql(sql, method, tenantId):
    # args = ProjectArgs(projectId)
    # proxies = args.get_proxy_list()
    # # dynamodb = DynamoDB()
    # # result = dynamodb.scanTable({
    # #     "table_name": "resource",
    # #     "limit": 100000,
    # #     "expression": Attr("projectId").eq(projectId),
    # #     "start_key": ""
    # # })["data"]
    # ip = "192.168.16.117"
    # if len(proxies) > 0:
    #     ip = proxies[0]
    

    response = ssm.get_parameter(
        Name=tenantId,
    )
    value = json.loads(response["Parameter"]["Value"])
    conn = http.client.HTTPConnection(host=value["olap"]["PrivateIp"], port="8123")
    url = urllib.parse.quote("/ch/?query=" + sql, safe=":/?=&")
    conn.request(method, url)
    res = conn.getresponse()
    return res.read().decode("utf-8")


def lambda_handler(event, context):
    # 直接转proxy转发
    args = eval(event["body"])
    # res = executeSql(args["query"], "GET", args["projectId"])
    res = executeSql(args["query"], "GET", args["tenantId"])

    rows = filter(lambda x: x != '', res.split("\n"))

    # 这里没有任何的错误处理
    columns = args["schema"]

    final_res = []
    for row in rows:
        cells = row.split("\t")

        tmp = {}
        for index in range(len(cells)):
            tmp[columns[index]] = cells[index]

        final_res.append(tmp)

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(final_res, ensure_ascii=False)
    }