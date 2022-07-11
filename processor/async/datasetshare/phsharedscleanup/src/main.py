import boto3
from boto3.dynamodb.conditions import Key

'''
args:
    event = {
        "projectId": "Dp10sMiAYXWxRZj",
        "owner": "xx",
        "showName": "xx",
        "tenantId": "",
        "shares": [
            {
                "target": "ds name", // 共享时的目标DS 名称
                "targetCat": "catalog | intermediate | uploaded", // 共享时的目标DS的类型  catalog是数据目录  intermediate是结果数据集  uploaded 是上传的数据 都需要分别处理
                "targetPartitionKeys": [
                    {
                        "name": "key1",
                        "type": "string"
                    },
                    {
                        "name": "key2",
                        "type": "string"
                    }
                ],
                "sourceSelectVersions": ["version1", "version2", "version3"]
                "source": "ds name", // 共享时的源DS 名称
            }
        ],
        "error": {
            "Error": "",
            "Cause": ""
        }
    }
'''

dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1")


def query_dataset(project_id, ds_name):
    return dynamodb.Table("dataset").query(
        IndexName="dataset-projectId-name-index",
        KeyConditionExpression=Key("projectId").eq(project_id) & Key("name").eq(ds_name)
    )["Items"][0]


def roll_back_version(id, versions):
    for version in versions:
        dynamodb.Table("version").delete_item(Key={"id": id, "name": version})


def lambda_handler(event, context):
    errors = event.get("errors")

    project_id = event["projectId"]

    for item in event["shares"]:
        ds_id = query_dataset(project_id, item["target"])["id"]
        roll_back_version(f"{project_id}_{ds_id}", item["sourceSelectVersions"])

    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
        }
    }
