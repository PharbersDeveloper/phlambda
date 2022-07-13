import os
import json
import boto3
from datetime import datetime
from collections import deque
# from cal import calDatasetPath, calDatasetPathOne
from sample import create_sample_args
from share import create_share_args
#from args import *
#from sms import *
# from args import *
# from sms import *
dynamodb = boto3.resource('dynamodb')

def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,
                     jobCat='notification', jobDesc='executionSuccess', message='', status='prepare',
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
            'code': code,
            'date': date,
            'category': category,
            'owner': owner
        }
    )
    return response


# def creat_args(event, stackargs, stacksm, datasets, jobs, links, dagName):
#     recursive = event['calculate'].get('recursive', True)
#     print("recursive>>>>>>>")
#     print(recursive)
#     args = {}
#     sm = {}
#     if recursive:
#         if (calDatasetPath(event['calculate']['name'], datasets, jobs, links, stackargs)):
#             stack2smargs(stackargs, event, args)

#         if (calDatasetPath(event['calculate']['name'], datasets, jobs, links, stacksm)):
#             prevJobName = 'StateMachineStartHook'
#             stack2smdefs(stacksm, event, sm, prevJobName)
#     else:
#         if (calDatasetPathOne(event['calculate']['name'], datasets, jobs, links, stackargs)):
#             stack2smargs(stackargs, event, args)

#         if (calDatasetPathOne(event['calculate']['name'], datasets, jobs, links, stacksm)):
#             prevJobName = 'StateMachineStartHook'
#             stack2smdefs(stacksm, event, sm, prevJobName)

#     s3 = boto3.client('s3')
#     s3.put_object(
#         Body=json.dumps(sm).encode(),
#         Bucket='ph-platform',
#         Key='2020-11-11/jobs/statemachine/pharbers/' + dagName + "/" +event['runnerId'] + '.json'
#     )
#     return args


# def create_ds_args(event, ts):

#     # 1. put notification
#     put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], dynamodb=dynamodb)

#     # 2. generator execution args
#     # TODO: create args and state machine files
#     table = dynamodb.Table('dag')
#     items = table.query(
#         Select='ALL_ATTRIBUTES',
#         Limit=1000,
#         ExpressionAttributeValues={
#             ':v1': event['projectId']
#         },
#         KeyConditionExpression='projectId=:v1'
#     )['Items']

#     datasets = list(filter(lambda x: x['ctype'] == 'node' and x['cat'] == 'dataset', items))
#     jobs = list(filter(lambda x: x['ctype'] == 'node' and x['cat'] == 'job', items))
#     links = list(filter(lambda x: x['ctype'] == 'link', items))
#     links = list(map(messageAdapter, links))
#     stackargs = deque()
#     stacksm = deque()
#     dagName = ("_").join(event['runnerId'].split("_")[:-1])

#     args = creat_args(event, stackargs, stacksm, datasets, jobs, links, dagName)

#     return {
#         'args': args,
#         'sm': '2020-11-11/jobs/statemachine/pharbers/' + dagName + "/" + event['runnerId'] + '.json'
#     }


def map_calculate_mode(mode, event, ts):

    map_dict = {
        "sample": create_sample_args,
        "share": create_share_args
    }
    try:
        msg = map_dict[mode](event, ts)
        return msg
    except Exception as e:
        print("*"*50 + " ERROR " + "*"*50 + "\n" + str(e))
        raise Exception("Wrong trigger")


def lambda_handler(event, context):
    # cicd 0701 1608
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    msg = map_calculate_mode(mode=event["calculate"]["type"], event=event, ts=ts)

    #if event["calculate"]["type"] != "sample":
    #    raise Exception("Wrong trigger")
    #msg = create_sample_args(event, ts)
    
    # if event["calculate"].get("type") == "sample":
    #     msg = create_sample_args(event, ts)
    # else:
    #     msg = create_ds_args(event,ts)


    return msg
