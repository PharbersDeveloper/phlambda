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

IndexTables = ['scenario', 'dataset',  'dagconf', 'dag', 'action', 'notification', 'dashboard', 'execution', 'executionStatus', 'logs', 'scenario_trigger', 'scenario_step', 'step', 'slide', 'version']

def query_table_item(tableName, QueryKey, Queryvalue):
    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table(tableName)
    #------- table scheam -----------------------#
    tableScheam = ds_table.key_schema
    tableScheam = list(map(lambda x:  {'PartitionKey': x['AttributeName']} if x['KeyType'] == 'HASH' else {'SortKey': x['AttributeName']}, tableScheam))
    tableScheamDict = {**tableScheam[0], **tableScheam[1]}
    indexs_of_table = ds_table.global_secondary_indexes
    if indexs_of_table is None:
        return None, None
    else:
        #-----------table index------------------#
        IndexName = indexs_of_table[0]['IndexName']
        KeySchema = indexs_of_table[0]['KeySchema']
        KeySchema = list(map(lambda x:  {'PartitionKey': x['AttributeName']} if x['KeyType'] == 'HASH' else {'SortKey': x['AttributeName']}, KeySchema))
        MapKeyDict = {**KeySchema[0], **KeySchema[1]}
        if IndexName == 'dataset-projectId-name-index':
            res = ds_table.query(
                IndexName=IndexName,
                KeyConditionExpression=Key(MapKeyDict['PartitionKey']).eq(Queryvalue)
            )
            return res['Items'], tableScheamDict
        elif tableScheamDict['PartitionKey'] == str(QueryKey):
            res = ds_table.query(
                KeyConditionExpression=Key(MapKeyDict['PartitionKey']).eq(Queryvalue)
            )
            return res['Items'], tableScheamDict
        else:
            return None, None

def del_table_item(tableName, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    delItem = dict(kwargs.items())
    table = dynamodb.Table(tableName)
    table.delete_item(
        Key=delItem,
    )

def lambda_handler(event, context):

    projectId = event['projectId']

    result = {}
    try:
        count = 0
        sum_of_tables = len(IndexTables)
        #------------------获取表中含index的Items数据--------------------------------------#
        for table in IndexTables:
            ItemsOfTable, tableSchemaDict = query_table_item(table, 'projectId', projectId)
            currentNum = count + 1
            if ItemsOfTable is None and tableSchemaDict is None:
                pass
            else:
                print(f"正在删除第{str(str(currentNum))}张表数据: {table}, 还剩{str(sum_of_tables-currentNum)}张表")
                #-------------删除表中Item-------------------------------------#
                for item in ItemsOfTable:
                    del_item ={}
                    del_item[tableSchemaDict['PartitionKey']] = item[tableSchemaDict['PartitionKey']]
                    del_item[tableSchemaDict['SortKey']] = item[tableSchemaDict['SortKey']]
                    del_table_item(table, **del_item)
        result['status'] = 'ok'
        result['message'] = 'delete success'
    except Exception as e:
        print('*'.join(['*'*50, 'ERORR', '*'*50]) +'\n' + str(e))
        result['status'] = 'error'
        result['message'] = str(e)
    return result
