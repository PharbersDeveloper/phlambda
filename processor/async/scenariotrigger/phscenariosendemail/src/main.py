import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
import time
from sendemail import SendEmail
from datetime import datetime, timedelta


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

def ChangeStrToDict(data):
    return json.loads(data) if isinstance(data, str) else data

def QueryAllItemsOfDyTable(tableName, partitionKey, ValueOfpartitionKey):

    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table(tableName)
    res = ds_table.query(
        KeyConditionExpression=Key(partitionKey).eq(ValueOfpartitionKey)
    )

    return res["Items"]


def query_item_of_dyTable(tableName, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    ds_table = dynamodb.Table(tableName)
    res = ds_table.get_item(
        Key=kwargs
    )
    try:
        item = res["Item"]
    except:
        item = []
    return item

def turn_decimal_into_int(data):
    return int(data) if isinstance(data, Decimal) else data


#---- 线上时间转换成标准时间-> Asia/Shanghai -------#
def time_transformate(timestamp):
    from pytz import timezone
    import datetime
    tz = timezone("Asia/Shanghai")
    timestamp = float(timestamp/1000)
    result = tz.fromutc(datetime.datetime.utcfromtimestamp(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
    return result



def handleResultData(ResultData, showName):

    ResultList = []
    for result in ResultData:
        tmp = {}
        tmp['runnerId'] = result[0]['runnerId']
        tmp['showName'] = showName
        tmp['stepName'] = result[-1]['name']
        tmp['BasicInfo'] = ChangeStrToDict(result[-1]['detail'])
        tmp['stepIndex'] = turn_decimal_into_int(result[-1]['index'])
        tmp['startTime'] = time_transformate(result[0]['date'])
        tmp['endTime'] = time_transformate(result[0]['stopdate'])
        tmp['status'] = result[1]['status']
        tmp['Error'] = ChangeStrToDict(ChangeStrToDict(result[1]['message'])['cnotification']['error']) if result[1]['status'] == 'failed' else ' '
        ResultList.append(tmp)
    return ResultList

def get_ScenarioId(BasicData):
    try:
        ScenarioId = (BasicData[0]).get("scenarioId")
    except:
        ScenarioId = None
    return ScenarioId

def lambda_handler(event, context):

    print("*"*50 + "Event" + "*"*50)
    print(event)
    try:
        #1. 通过当前的tranceid 在scenario execution 表中找到所有对应的 runner id
        DataOfExecution = get_Item_of_dyTable('scenario_execution', 'traceId-scenarioId-index', event['traceId'])
        print("*"*50 + "DataOfExecution" + "*"*50)
        print(DataOfExecution)
        #3. 在scenario step 表中读到基本信息
        BasicInfo = list(map(lambda x: query_item_of_dyTable('scenario_step', **{'scenarioId': x.get('scenarioId'), 'id': x.get('stepId')}), DataOfExecution))
        print("*"*50 + "BasicInfo" + "*"*50)
        print(BasicInfo)



        #2. 通过runnerid 以及当前的 projectid 在 notification中找到 当前runnerid的运行结果
        DataOfNotification = list(map(lambda x: query_item_of_dyTable('notification', **{'id': x['runnerId'], 'projectId': event['projectId']}), DataOfExecution))
        print("*"*50 + "DataOfNotification" + "*"*50)
        print(DataOfNotification)

        ResultData = list(zip(DataOfExecution, DataOfNotification, BasicInfo))
        showName = event['showName']
        Result = handleResultData(ResultData, showName)
        print("*"*50 + "Result" + "*"*50)
        print(Result)

        ScenarioId =get_ScenarioId(BasicData=BasicInfo)
        if ScenarioId is None:
            print("scenarioId not exits!")
            pass
        else:
            #---- 查scenario_report获取 接受邮箱地址 ---------#
            reportItmes = QueryAllItemsOfDyTable('scenario_report', "scenarioId", ScenarioId)
            #----基于acrtive 对email 过滤 -------------------#
            report_emails = [ChangeStrToDict(x.get("detail")).get("destination") for x in reportItmes if x.get("active") is True]
            #report_emails = list(filter(lambda x:  ChangeStrToDict(x.get("detail")).get("destination"), reportItmes))
            #--- 去重 ----#
            to_emails = list(set(report_emails))
            to_emails.sort(key=report_emails.index)
            if len(list(to_emails)) != 0:
                ToNickName = "Hello, Stranger!"  #接受邮箱昵称
                SendEmail(Result, ToNickName, to_emails)

    except Exception as e:
        print("*"*50 + "Error" + "*"*50)
        print(e)

    return True
