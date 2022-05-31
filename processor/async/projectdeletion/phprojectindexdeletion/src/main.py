import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

'''
删除索引
包括表：
1. Scenario
2. Datasets
3. dagconf
4. dag
5. resource （*现在还没有*）
6. action
7. notification
8. dashboard
9. exectuion
10. executionStatus
11. logs
12. scenario_trigger
13. scenario_step
14. step
15. slide
16 version

args = {
    "traceId": "alfred-resource-creation-traceId",
    "projectId": "ggjpDje0HUC2JW",
    "projectName": "demo",
    "owner": "alfred",
    "showName": "alfred"
}
'''

_IndexTables = ['scenario', 'Datasets',  'dagconf', 'dag', 'action', 'notification', 'dashboard', 'exectuion', 'executionStatus', 'logs', 'scenario_trigger', 'scenario_step', 'step', 'slide', 'version']

def query_table_item(tableName, QueryKey, Queryvalue):
    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table(tableName)
    res = ds_table.query(
        KeyConditionExpression=Key(QueryKey).eq(Queryvalue)
    )
    return res["Items"]

def del_table_item(tableName, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    delItem = dict(kwargs.items())
    table = dynamodb.Table(tableName)
    table.delete_item(
        Key=delItem,
    )

def cause_decimal_to_int(dataOfDict):
    keys = list(dataOfDict.keys())
    for key in keys:
        if isinstance(dataOfDict[key], Decimal):
            dataOfDict[Key] = int(dataOfDict[Key])
    return dataOfDict


#----------tableName需小写--------------------------#
IndexTables = [str(x).lower() for x in _IndexTables]

def lambda_handler(event, context):

    projectId = event['projectId']

    result = {}
    try:
        count = 0
        sum_of_tables = len(IndexTables)
        #------------------获取表中含index的Items数据--------------------------------------#
        for table in IndexTables:
            ItemsOfTable = query_table_item(table, 'projectId', projectId)
            currentNum = count + 1
            print(f"正在删除第{str(str(currentNum))}张表数据: {table}, 还剩{str(sum_of_tables-currentNum)}张表")
            #-------------删除表中Item-------------------------------------#
            for item in ItemsOfTable:
                item = cause_decimal_to_int(item)
                del_table_item(table, **item)
        result['status'] = 'ok'
        result['message'] = 'delete success'
    except Exception as e:
        print('*'.join(['*'*50, 'ERORR', '*'*50]) +'\n' + str(e))
        result['status'] = 'error'
        result['message'] = str(e)
    return result





