import json
import boto3
import math
import datetime
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal

''''
1. 通过当前的tranceid 在scenario execution 表中找到所有对应的 runner id
2. 通过runnerid 以及当前的 projectid 在 notification中找到 当前runnerid的运行结果
2.1 如果正确，只读运行状态
2.2 如果错误，需要解析你上次写的错误
3. 在scenario step 表中读到基本信息
4. 将基本信息语状态或错误信息，拼接成一个html 发送给固定邮件 alfredyang@pharbers.com
其基本信息包括：step index， detail里面的type， 是否递归执行，以及计算数据集的名称
其状态信息包括：开始执行时间，结束执行时间，执行成功与否，以及错误信息
'''

'''
event={"traceId.$":"$.common.traceId",
       "projectId.$":"$.common.projectId",
       "owner.$":"$.common.owner",
       "showName.$":"$.common.showName",
       "jobCat.$":"$.action.cat",
       "jobDesc.$":"$.action.desc",
       "comments.$":"$.action.comments",
       "message.$":"$.message"
       }
'''
def get_Item_of_dyTable(tableName, IndexName, traceId):
    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table(tableName)
    res = ds_table.query(
        IndexName=IndexName,
        KeyConditionExpression=Key('traceId').eq(traceId)
    )
    return res['Items']

def query_item_of_dyTable(tableName, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table(tableName)
    res = ds_table.query(
        key=kwargs
    )
    try:
        item = res["Items"]
    except:
        item = []
    return item

def get_per_status_of_execution(projectId, runnerIds):
    tmpList = []
    for runnerId in runnerIds:
        tmpData = query_item_of_dyTable('notification', **{'id': runnerId, 'projectId': projectId})
        tmpList.append(tmpData)
    return tmpList

def lambda_handler(event, context):

    #1. 通过当前的tranceid 在scenario execution 表中找到所有对应的 runner id
    DataOfExecution = get_Item_of_dyTable('scenario_execution', 'traceId-scenarioId-index', event['traceId'])

    #3. 在scenario step 表中读到基本信息
    BasicInfo = list(map(lambda x: query_item_of_dyTable('scenario_step', **{'scenarioId': x.get('scenarioId'), 'id': x.get('stepId')}), DataOfExecution))

    RunnerIds = list(map(lambda x: x['runnerId'], DataOfExecution))
    #2. 通过runnerid 以及当前的 projectid 在 notification中找到 当前runnerid的运行结果
    DataOfNotification = get_per_status_of_execution(event['projectId'], RunnerIds)

    #4. 将基本信息语状态或错误信息，拼接成一个html 发送给固定邮件 alfredyang@pharbers.com
    #其基本信息包括：step index， detail里面的type， 是否递归执行，以及计算数据集的名称
    #其状态信息包括：开始执行时间，结束执行时间，执行成功与否，以及错误信息

    #---TODO 具体邮件包含信息需要解析后拼成html，明天做, scenario_execution 表中还需要加入stepId字段
    StatusResult = list(zip(DataOfExecution, DataOfNotification, BasicInfo))

    return True
