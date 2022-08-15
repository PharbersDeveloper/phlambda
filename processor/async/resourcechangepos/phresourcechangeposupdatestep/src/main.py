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


def update_step_item(dagItems):

    # for delete_item in dagItems["insertItems"]:
    table.delete_item(
        Key={
            "projectId": dagItems["pjName"],
            "sortVersion": dagItems["stepId"]
        }
    )

    # for insert_item in dagItems["deleteItems"]:
    res = table.put_item(
        Item=dagItems
    )


def lambda_handler(event, context):
    print(event)
    deleteItems = query_table(event.get("pjName"), event.get("stepId"))
    update_step_item(event)

    return {
        "deleteItems": deleteItems,
        "insertItems": event
    }
