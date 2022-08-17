import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("step")


def query_table(pjName, stepId):
    response = table.query(
        KeyConditionExpression=Key("pjName").eq(pjName) & Key("stepId").eq(stepId),
    )
    return response.get("Items")[0]


def update_step_item(stepItem):

    # for delete_item in stepItems["insertItems"]:
    table.delete_item(
        Key={
            "pjName": stepItem["pjName"],
            "stepId": stepItem["stepId"]
        }
    )

    # for insert_item in stepItems["deleteItems"]:
    res = table.put_item(
        Item=stepItem
    )


def lambda_handler(event, context):
    print(event)
    stepItem = event["step"]
    deleteItems = query_table(stepItem.get("pjName"), stepItem.get("stepId"))
    update_step_item(event)

    return {
        "deleteItems": deleteItems,
        "insertItems": event
    }
