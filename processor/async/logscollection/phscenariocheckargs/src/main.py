import json
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")


def get_uuid():
    uu_id = uuid.uuid4()
    suu_id = ''.join(str(uu_id).split('-'))
    return suu_id


def lambda_handler(event, context):
    print(event)

    event["common"]["traceId"] = get_uuid()
    event["common"]["name"] = event.get("jobName")
    event["type"] = "execution"
    return event
