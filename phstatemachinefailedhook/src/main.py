import os
import json
import boto3
from datetime import datetime
# from phmetrixlayer import aws_cloudwatch_put_metric_data

def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,  
    jobCat='notification', jobDesc='executionSuccess', message='', status='failed',
    dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('notification')
    response = table.put_item(
       Item={
            'id': runnerId,
            'projectId': projectId,
            'showName': showName,
            'status': status,
            'jobDesc': jobDesc,
            'comments': comments,
            'message': message,
            'jobCat': jobCat,
            'code': code,
            'category': category,
            'owner': owner
        }
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

def errorHandle(error, runnerId):
    # 1. 看看是不是gen dag的错误，也就是说不能两个runnid 同时执行
    # error = event['error']
    print('=======> alfred test')
    print(error)
    if 'genDagError' in error and error['genDagError']['Error'] == 'AlreadyExistsException':
        return error['genDagError']['Cause']        
    
    # 2. 看看是不是dag的错误
    if 'executeError' in error:
        executionArn = ':'.join(['arn:aws-cn:states:cn-northwest-1:444603803904:execution', runnerId, runnerId])
        client = boto3.client('stepfunctions')
        events = client.get_execution_history(executionArn=executionArn)['events']
        eventsCount = len(events)
        errorEvent = events[eventsCount - 1]
        detail = json.loads(errorEvent['executionFailedEventDetails']['cause'])
        print(detail)
        return json.dumps(detail['Step']['Status'])

    raise Exception('unknown')

def lambda_handler(event, context):
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

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

    message = ''
    try:
        message = errorHandle(event['error'], event['runnerId'])
    except:
        message = 'unknown'
        
    for item in items:
        if item['projectId'] == event['projectId']:
            put_notification(item['id'], item['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], status ='failed', message=message)
        else:
            if item['status'] == 'running':
                put_notification(item['id'], item['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], status ='failed')
            elif item['status'] == 'queued':
                put_notification(item['id'], item['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], status ='canceled')
    
    return { "status": "ok"  }