import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key
from logpath import *
# from phmetrixlayer import aws_cloudwatch_put_metric_data


def put_notification(jobShowName, jobName, runnerId, projectId, category, code, comments, date, owner, showName,
    jobCat='notification', jobDesc='executionSuccess', message='', status='success',
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
            "jobName": jobName,
            "runId": runnerId,
            "jobShowName": jobShowName
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
            'date': date,
            'code': code,
            'category': category,
            'owner': owner
        }
    )

    return response


def put_start_execution(jobShowName, jobName, projectId, runnerId, owner, date, desc, logs, status='success', dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    jobIndex = '_'.join([date, jobName])
    startAt = date
    endAt = ""
    dagName = ("_").join(runnerId.split("_")[:-1])
    id = '_'.join([jobIndex, projectId])
    #TODO pharbers为租户id
    executionTemplate = f"s3://ph-platform/2020-11-11/jobs/statemachine/pharbers/{dagName}/{runnerId}.json"

    execution_table = dynamodb.Table('execution')
    response = execution_table.put_item(
        Item={
            'jobIndex': jobIndex,
            'projectId': projectId,
            'status': status,
            'desc': desc,
            'jobShowName': jobShowName,
            'jobName': jobName,
            'startAt': startAt,
            'endAt': endAt,
            'logs': logs,
            'runnerId': runnerId,
            'id': id,
            'owner': owner,
            'executionTemplate': executionTemplate
        }
    )
    return response


# def put_success_execution(runnerId, jobName, date, logs, status, dynamodb=None):
#     # 首先从dynamodb的execution表获取item
#     if not dynamodb:
#         dynamodb = boto3.resource('dynamodb')
#     execution_table = dynamodb.Table('execution')

#     res = execution_table.query(
#         IndexName='runnerId-jobName-index',
#         KeyConditionExpression=Key("runnerId").eq(runnerId)
#                                & Key("jobName").begins_with(jobName)
#     )
#     item = res["Items"][0]

#     # 更改status和endAt
#     item.update({"endAt": date})
#     item.update({"status": status})
#     item.update({"logs": logs})

#     response = execution_table.put_item(
#         Item=item
#     )
#     return response


# def put_metrics(runnerId, projectId, projectName, currentUserId, currentName, action="dag_execution_end"):
#     aws_cloudwatch_put_metric_data(projectId, projectName,
#                                     currentUserId,
#                                     currentName,
#                                     action,
#                                     runnerId, # action_detail,
#                                     1,
#                                     'Count')


def lambda_handler(event, context):
    print(event)
    dt = datetime.now()
    ts = datetime.timestamp(dt) * 1000

    pn = event['projectName']
    jobShowName = event["jobName"]

    flowVersion = 'developer'
    tmpJobName = '_'.join([pn, pn, flowVersion, event['jobName']])
    status = event['status']

    # 3. put execution
    if status == "running":
        put_start_execution(jobShowName, tmpJobName, event['projectId'], event['runnerId'], event['owner'], str(int(ts)), "", "", status=status)
    else:
        # stepId = event.get("stepId")
        # clusterId = event.get("clusterId")
        # logs = get_log_path(stepId, clusterId)
        put_success_execution(event['runnerId'], tmpJobName, str(int(ts)), "", status)

    # 1. put notification
    put_notification(jobShowName, tmpJobName, event['runnerId'], tmpJobName, None, 0, "", str(int(ts)), event['owner'], event['showName'], status = status)
    # 2. put metrics
    # put_metrics(event["runnerId"], pid, event['projectName'], event["owner"], event["showName"], action = hid)



    return {
        "status": "ok"
    }
