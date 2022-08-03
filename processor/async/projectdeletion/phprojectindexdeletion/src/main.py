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
#---- !!! 注：DynamoDB 表无二级索引时，默认分区键为 projectId   ------------#
#TODO 部分结构不满足projectId作为分区键or不存在二级索引，目前先过滤掉
filterTables = ['executionStatus', 'logs', 'slide']
IndexTables = ['scenario', 'dataset',  'dagconf', 'dag', 'action', 'notification', 'dashboard', 'execution', 'executionStatus', 'logs', 'step', 'slide', 'version']
IndexTables = [x for x in IndexTables if x not in filterTables]

#----- dynamoDB 二级索引 ------#
IndexList = ['dataset-projectId-name-index', 'dag-projectId-name-index', 'notification-traceId-id-index', 'runnerId-jobName-index','id-index-index', 'dagconf-projectId-id-indexd', 'version-projectId-name-index']

#------ 处理空Item -----------#
def handleQueryResponse(resp):
    print("*"*50 + " query  response  " + "*"*50 + "\n", str(resp))
    try:
        if len(resp['Items']) == 0:
            return None
        else:
            return resp['Items']
    except Exception as e:
        print("*"*50 + " query dynamoDB error " + "*"*50 + "\n", str(e))
        return None


def query_table_item(tableName, QueryKey, Queryvalue):
    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table(tableName)
    #------- table scheam -----------------------#
    tableScheam = ds_table.key_schema
    tableScheam = list(map(lambda x:  {'PartitionKey': x['AttributeName']} if x['KeyType'] == 'HASH' else {'SortKey': x['AttributeName']}, tableScheam))
    tableScheamDict = {**tableScheam[0], **tableScheam[1]}
    indexs_of_table = ds_table.global_secondary_indexes

    if tableScheamDict['PartitionKey'] == str(QueryKey):
        res = ds_table.query(
            KeyConditionExpression=Key(str(QueryKey)).eq(Queryvalue)
        )
        return handleQueryResponse(res), tableScheamDict
    elif indexs_of_table is not None:
        #-----------table index------------------#
        print("*"*50 + "IndexName" + "*"*50, indexs_of_table)
        IndexName = indexs_of_table[0]['IndexName']
        KeySchema = indexs_of_table[0]['KeySchema']
        KeySchema = list(map(lambda x:  {'PartitionKey': x['AttributeName']} if x['KeyType'] == 'HASH' else {'SortKey': x['AttributeName']}, KeySchema))
        MapKeyDict = {**KeySchema[0], **KeySchema[1]}
        if IndexName in IndexList:
            res = ds_table.query(
                IndexName=IndexName,
                KeyConditionExpression=Key(MapKeyDict['PartitionKey']).eq(Queryvalue)
            )
            return handleQueryResponse(res), tableScheamDict
        else:
            return None, None

def del_table_item(tableName, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    delItem = dict(kwargs.items())
    table = dynamodb.Table(tableName)
    table.delete_item(
        Key=delItem,
    )

def TraverseDelete(TraverseTables, Partitionkey, PartitionkeyValue):
    sum_of_tables = len(TraverseTables)
    count = 0
    #------------------获取表中含index的Items数据--------------------------------------#
    for table in TraverseTables:

        ItemsOfTable, tableSchemaDict = query_table_item(table, Partitionkey, PartitionkeyValue)
        count = count + 1
        if ItemsOfTable is None:
            print(f" the item of {table}  is empty.")
            pass
        else:
            #----- 基于scenario表的处理 --------------------#
            if table == "scenario":
                for item in ItemsOfTable:
                    ScenarioId = item["id"]
                    TraverseDelete(TraverseTables=['scenario_trigger', 'scenario_step','scenario_execution'], Partitionkey="scenarioId", PartitionkeyValue=ScenarioId)
            #----- 基于scenario表的处理 --------------------#

            print(f"正在删除第{str(str(count))}张表数据: {table}, 还剩{str(sum_of_tables-count)}张表")
            #-------------删除表中Item-------------------------------------#
            for item in ItemsOfTable:
                del_item ={}
                del_item[tableSchemaDict['PartitionKey']] = item[tableSchemaDict['PartitionKey']]
                del_item[tableSchemaDict['SortKey']] = item[tableSchemaDict['SortKey']]
                del_table_item(table, **del_item)

def lambda_handler(event, context):

    projectId = event['projectId']
    print("*"*50 + " event " + "*"*50 + "\n", event)

    result = {}
    try:
        TraverseDelete(IndexTables, 'projectId', projectId)
        '''
        sum_of_tables = len(IndexTables)
        #------------------获取表中含index的Items数据--------------------------------------#
        for table in IndexTables:
            ItemsOfTable, tableSchemaDict = query_table_item(table, 'projectId', projectId)
            count = count + 1
            if ItemsOfTable is None:
                print(f" the item of {table}  is empty.")
                pass
            else:
                print(f"正在删除第{str(str(count))}张表数据: {table}, 还剩{str(sum_of_tables-count)}张表")
                #-------------删除表中Item-------------------------------------#
                for item in ItemsOfTable:
                    del_item ={}
                    del_item[tableSchemaDict['PartitionKey']] = item[tableSchemaDict['PartitionKey']]
                    del_item[tableSchemaDict['SortKey']] = item[tableSchemaDict['SortKey']]
                    del_table_item(table, **del_item)
        '''
        result['status'] = 'ok'
        result['message'] = 'delete success'
    except Exception as e:
        print('*'.join(['*'*50, 'ERORR', '*'*50]) +'\n' + str(e))
        result['status'] = 'error'
        result['message'] = str(e)
    return result
