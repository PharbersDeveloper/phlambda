import json
import boto3
import math
import datetime
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')

'''
将错误提取出来写入到notification中
args:
    event = {
                "projectId": "ggjpDje0HUC2JW",
                "traceId": "",
                "projectName": "demo",
                "owner": "alfred",
                "showName": "alfred",
                "error": {
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
scenarioId
runnerId
date:
runtime:      manual / timer / dataset change
owner:
reporter
'''


def query_table_item(tableName, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table(tableName)
    res = ds_table.get_item(
        Key=kwargs,
    )
    try:
        Item = res["Item"]
    except:
        Item = {}
    return Item



def lambda_handler(event, context):

    ds_table = dynamodb.Table('scenario_execution')


    #----------- 记录每个exectuion 执行的开始时间和结束时间 -------------#

    item_of_execution = query_table_item('scenario_execution',
                                         scenarioId=event['scenarioId'],
                                         runnerId=event['runnerId'])

    if len(item_of_execution) == 0:
        #----- execution 开始 -------#
        response = ds_table.put_item(
            Item={
                'scenarioId': event['scenarioId'],
                'runnerId': event['runnerId'],
                'date': math.floor(datetime.datetime.now().timestamp() * 1000),
                'runtime': event['runtime'],
                'owner': event['owner'],
                'reporter': event['reporter'],
                'traceId': event['traceId'],
                'stepId': event['stepId']
            }
        )
    else:
        #----- execution 结束 -------#
        item_of_execution['stopdate'] = math.floor(datetime.datetime.now().timestamp() * 1000),
        response = ds_table.put_item(
            Item=item_of_execution
        )

    return True
