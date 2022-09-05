import os
import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
# from phmetrixlayer import aws_cloudwatch_put_metric_data

def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,  
    jobCat='notification', jobDesc='executionSuccess', message='', status='queued',
    dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    message = {
        "type": "operation",
        "opname": owner,
        "projectId": projectId,
        "cnotification": {
            "data": "{}",
            "error": "{}",
            "runId": runnerId
        }
    }

    table = dynamodb.Table('notification')
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
                'comments': comments,
                'message': json.dumps(message, ensure_ascii=False),
                'jobCat': jobCat,
                'date': date,
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


# def put_metrics(runnerId, projectId, projectName, currentUserId, currentName, action="dag_execution_end"):
#     aws_cloudwatch_put_metric_data(projectId, projectName,
#                                     currentUserId,
#                                     currentName,
#                                     action,
#                                     runnerId, # action_detail,
#                                     1,
#                                     'Count')

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
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(tableName)
            response = table.put_item(
                Item={
                    'projectId': oldItem["projectId"],
                    'date': oldItem['date'],
                    'current': oldItem['current'],
                    'runnerId': oldItem["runnerId"],
                    'owner': oldItem["owner"],
                    'status': Status
                }
            )
    return response



def lambda_handler(event, context):
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    if event['stage'] == 'start':
        pid = event['projectId']
        pn = event['projectName']
        flowVersion = 'developer'

        # 1. put notification for dag
        put_notification(event['runnerId'], pid, None, 0, "", int(ts), event['owner'], event['showName'], status='running')
        # 2. put notification for every job
        for iter in event['Input'].keys():
            if iter == 'common':
                continue

            tmpJobName = '_'.join([pn, pn, flowVersion, iter])
            put_notification(event['runnerId'], tmpJobName, None, 0, "", int(ts), event['owner'], event['showName'])
        #---- running -----#
        put_item(tableName="executionStatus", event=event, Status="running")
        
    else:
        pid = event['projectId']
        # 1. put notification for dag
        put_notification(event['runnerId'], pid, None, 0, "", int(ts), event['owner'], event['showName'], status='success')
        #---- success -----#
        put_item(tableName="executionStatus", event=event, Status="success")

    return { "status": "ok"  }

