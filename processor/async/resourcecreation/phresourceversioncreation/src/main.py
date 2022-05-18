import time
import boto3
from boto3.dynamodb.conditions import Key

'''
这个函数做一件事情写入dataset dynamodb
args = {
    "traceId": "String",
    "projectId": "String",
    "owner": "String",
    "showName": "String",
    "datasets": [
        {
            "name": "String",
            "cat": "intermediate",
            "format": "parquet",
            "schema": [{}],
            "version": ""
        }
    ]
}

return = event下的datasets
'''


def lambda_handler(event, context):
    print(event)

    db = boto3.resource("dynamodb")
    ds_table = db.Table("dataset")
    version_table = db.Table("version")

    if event["script"]["runtime"] == "dataset" and "name" not in event["script"]:
        for item in event["datasets"]:
            ds_result = ds_table.query(
                IndexName="dataset-projectId-name-index",
                KeyConditionExpression=Key("projectId").eq(event["projectId"]) & Key("name").eq(item["name"])
            )["Items"]
            ds_id = ds_result.pop()["id"]

            version_table.put_item(
                Item={
                    "id": f"{event['projectId']}_{ds_id}",
                    "name": item["version"],
                    "datasetId": ds_id,
                    "date": str(int(round(time.time() * 1000))),
                    "owner": event["owner"],
                    "projectId": event["projectId"]
                }
            )

    return True
