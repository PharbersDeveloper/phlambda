import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Attr,Key


'''

args = {
    "common": {
        "tranceId": "",
        "runnerId": "sample_sample_developer_2022-07-04T05:49:39+00:00",
        "projectId": "Dp10sMiAYXWxRZj",
        "projectName": "sample",
        "owner": "16dc4eb5-5ed3-4952-aaed-17b3cc5f638b",
        "showName": "赵浩博",
        "tenantId": "zudIcG_17yj8CEUoCTHg"
    },
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
    ]
}
'''


def get_ds_with_index(dsName, projectId):

    dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")
    ds_table = dynamodb_resource.Table('dataset')
    res = ds_table.query(
        IndexName='dataset-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").begins_with(dsName)
    )
    return res["Items"][0]

def put_to_version(id,name,datasetId,owner,projectId):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('version')

    response = table.put_item(
        Item={
            'id': id,
            'name': name,
            'datasetId': datasetId,
            'date': str(datetime.now().timestamp() * 1000),
            'owner': owner,
            'projectId': projectId,
        }
    )
    print(response)


def lambda_handler(event, context):
    print(event)

    for shareItem in event["calculate"]["shares"]:
        #---- query item of dataset -----------#
        datasetItem = get_ds_with_index(dsName=shareItem["target"], projectId=event["common"]["projectId"])

        versionId = event["common"]["projectId"] + "_" + datasetItem["id"]
        #----- update version -------------------#
        put_to_version(id=versionId, name=shareItem["version"], datasetId=datasetItem["id"], owner=event["common"]["owner"], projectId=event["common"]["projectId"])

    #----- update version -------------------#


    return {}
