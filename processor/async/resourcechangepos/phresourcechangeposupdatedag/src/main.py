import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal

'''
将错误提取出来写入到notification中
args:
    event = {
                "projectId": "ggjpDje0HUC2JW",
                "traceId": "",
                "projectName": "demo",
                "owner": "alfred",
                "showName": "alfred",
                "errors": {
                }
            },
return:
    {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
    }
}
'''


def lambda_handler(event, context):
    # 根据参数找到输入item 修改item的 name runtime traceId
    # 根据参数找到job item 修改item的 cmessage name runtime traceId
    # 根据参数找到输出item 修改item的 name runtime traceId
    return 1
