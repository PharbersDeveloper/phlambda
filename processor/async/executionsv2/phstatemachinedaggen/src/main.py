import json
import boto3
from datetime import datetime
from collections import deque
from notify import *
from calv2 import *
from argsv2 import *


dynamodb = boto3.resource('dynamodb')


def messageAdapter(x):
    x['ll'] = json.loads(x['cmessage'])
    return x


def build_execution_process(event, ts, dynamodb):

    # 1. put notification
    put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], dynamodb=dynamodb)

    # 2. generator execution args
    # TODO: create args and state machine files
    table = dynamodb.Table('dag')
    items = table.query(
        Select='ALL_ATTRIBUTES',
        Limit=1000,
        ExpressionAttributeValues={
            ':v1': event['projectId']
        },
        KeyConditionExpression='projectId=:v1'
    )['Items']

    datasets = list(filter(lambda x: x['ctype'] == 'node' and x['cat'] == 'dataset', items))
    jobs = list(filter(lambda x: x['ctype'] == 'node' and x['cat'] == 'job', items))
    links = list(filter(lambda x: x['ctype'] == 'link', items))
    links = list(map(messageAdapter, links))
    result = buildExecutionDag(datasets, jobs, links, event["calculate"]["name"], event["calculate"]["recursive"])
    result["args"] = extractJobArgs(result["jobs"], jobs, event)

    print(result)
    return result


def lambda_handler(event, context):
    # cicd 0717 1206
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    result = build_execution_process(event, ts, dynamodb)

    return result


if __name__ == "__main__":
    with open("../events/event.json", "r") as read_file:
        event = json.load(read_file)
        lambda_handler(event, None)
