import os
import json
import boto3
from datetime import datetime
# from logpath import get_log_path
from boto3.dynamodb.conditions import Key
# from phmetrixlayer import aws_cloudwatch_put_metric_data

def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,  
    jobCat='notification', jobDesc='executionSuccess', message='', status='failed',
    dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    dagName = ("_").join(runnerId.split("_")[:-1])
    jobShowName = projectId.strip(dagName + "_") if dagName in projectId else ""
    message = {
        "type": "operation",
        "opname": owner,
        "projectId": projectId,
        "cnotification": {
            "data": "{}",
            "error": "{}",
            "runId": runnerId,
            "jobShowName": jobShowName
        }
    }

    table = dynamodb.Table('notification')
    # 先判断notification是否存在 存在则进行更新
    res = table.query(
        KeyConditionExpression=Key("id").eq(runnerId)
                               & Key("projectId").begins_with(projectId)
    )
    if len(res["Items"]) == 0:
        response = table.put_item(
           Item={
                'id': runnerId,
                'projectId': projectId,
                'showName': showName,
                'status': status,
                'jobDesc': jobDesc,
                'date': date,
                'comments': comments,
                'message': json.dumps(message, ensure_ascii=False),
                'jobCat': jobCat,
                'code': code,
                'category': category,
                'owner': owner
            }
        )
    else:
        item = res["Items"][0]
        item.update({"status": status})
        response = table.put_item(Item=item)

    return response

def put_failed_execution(runnerId, jobName, date, logs, status, dynamodb=None):
    # 首先从dynamodb的execution表获取item
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    execution_table = dynamodb.Table('execution')

    res = execution_table.query(
        IndexName='runnerId-jobName-index',
        KeyConditionExpression=Key("runnerId").eq(runnerId)
                               & Key("jobName").begins_with(jobName)
    )
    item = res["Items"][0]

    # 更改status和endAt
    item.update({"endAt": date})
    item.update({"status": status})
    item.update({"logs": logs})

    response = execution_table.put_item(
        Item=item
    )
    return response

# def put_metrics(runnerId, projectId, projectName, currentUserId, currentName, action="dag_execution_end"):
#     aws_cloudwatch_put_metric_data(projectId, projectName,
#                                     currentUserId,
#                                     currentName,
#                                     action,
#                                     runnerId, # action_detail,
#                                     1,
#                                     'Count')

def handleTaskFailed(errorEvent):
    if 'executionFailedEventDetails' in errorEvent:
        return json.loads(errorEvent['executionFailedEventDetails']['cause'])
    elif 'cause' in errorEvent:
        return errorEvent['cause']
    else:
        return {"Step": {}}


def errorHandle(error, runnerId):
    # 1. 看看是不是gen dag的错误，也就是说不能两个runnid 同时执行
    # error = event['error']
    print('=======> alfred test')
    print(error)
    if 'genDagError' in error and error['genDagError']['Error'] == 'AlreadyExistsException':
        return error['genDagError']['Cause']        
    
    # 2. 看看是不是dag的错误
    if 'executeError' in error:
        stateMachineArn = ':'.join(['arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine', runnerId.replace(":", "-").replace("+", "-").replace("_","-")])
        client = boto3.client('stepfunctions')
        statemachine_events = client.list_executions(
            stateMachineArn=stateMachineArn
        )
        executionArn = statemachine_events["executions"][0]["executionArn"]
        events = client.get_execution_history(executionArn=executionArn)['events']
        eventsCount = len(events)
        errorEvent = events[eventsCount - 1]
        if errorEvent.get("type") == "ExecutionAborted":
            detail = {"Step": {}}
        else:
            detail = handleTaskFailed(errorEvent)
        print(detail)
        return json.dumps(detail['Step'])

    raise Exception('unknown')


def get_timeStamp(strTime):
    import time
    timeArray = time.strptime(strTime, "%Y-%m-%dT%H:%M:%S+00:00")
    timeStamp = str(int(time.mktime(timeArray)) * 1000)
    return timeStamp

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

def put_item(tableName, event, Status):

    if str(Status) == "running":
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(tableName)
        date = str(event["runnerId"]).split("_")[-1]
        response = table.put_item(
            Item={
                'projectId': event["projectId"],
                'date': date, #"runnerId 后面的时间",
                'current': get_timeStamp(date) + "_" + event["runnerId"], #date变时间搓 +  runnerId,
                'runnerId': event["runnerId"],
                'owner': event["showName"],
                'status': Status
            }
        )
    else:
        oldItem = query_table_item(tableName, id=event["projectId"], runnerId=event["runnerId"])
        if len(oldItem) == 0:
            print("item not exit")
            response = "item not exit"
        else:
            oldItem["status"] = Status
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(tableName)
            response = table.put_item(
                Item=oldItem
            )
    return response



def lambda_handler(event, context):
    # cicd 0717 1206
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt) * 1000

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('notification')
    items = table.query(
        Select='ALL_ATTRIBUTES',
        Limit=1000,
        ExpressionAttributeValues={
            ':v1': event['runnerId']
        },
        KeyConditionExpression='id=:v1'
    )['Items']

    err_message = ''
    try:
        err_message = errorHandle(event['error'], event['runnerId'])
    except:
        err_message = 'unknown'

    # step_id = ""
    # logs = "[]"
    # if json.loads(err_message).get("Id"):
        # step_id = json.loads(err_message).get("Id")
        # cluster_id = event["engine"]["id"]
        # logs = get_log_path(step_id, cluster_id)

    for item in items:
        if item['projectId'] == event['projectId']:
            put_notification(item['id'], item['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], status ='failed', message=err_message)
            # 失败的情况下修改status, endAt，logs
        else:

            if item['status'] == 'running':
                put_notification(item['id'], item['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], status ='failed')
                put_failed_execution(item['id'], item['projectId'], str(int(ts)), "", status="failed", dynamodb=None)
            elif item['status'] == 'queued':
                put_notification(item['id'], item['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], status ='canceled')

    put_item("executionStatus", event, "failed")
    return {
        "status": "ok"
    }
