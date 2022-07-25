import os
import json
import boto3
from phmetriclayer import aws_cloudwatch_put_metric_data
from datetime import datetime
from collections import deque
from sample import create_sample_args
from share import create_share_args

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

    aws_cloudwatch_put_metric_data(NameSpace="pharbers-platform",
                                   MetricName="platform-usage",
                                   tenantId=event["tenantId"])

    msg = map_calculate_mode(mode=event["calculate"]["type"], event=event, ts=ts)

    return msg
