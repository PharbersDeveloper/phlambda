import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Attr, Key


'''
args =  {
        "runnerId.$": "$.common.runnerId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "tenantId.$":"$.common.tenantId",
        "shares.$":"$.shares"
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


def put_dynamodb_item(table_name, item):

    dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")
    table = dynamodb_resource.Table(table_name)
    resp = table.put_item(
        Item=item
    )

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

    for shareItem in event["shares"]:
        #---- query item of dataset -----------#
        targetItem = get_ds_with_index(dsName=shareItem["target"], projectId=event["projectId"])

        versionId = event["projectId"] + "_" + targetItem["id"]
        #----- update version -------------------#
        for versionName in shareItem["sourceSelectVersions"]:
            put_to_version(id=versionId, name=versionName, datasetId=targetItem["id"], owner=event["owner"], projectId=event["projectId"])

        #----- update schema -------------------#
        targetSchema = json.loads(targetItem["target"]) if isinstance(targetItem["schema"], str) else targetItem["schema"]
        if len(targetSchema) == 0:
            sourceDsItem = get_ds_with_index(dsName=shareItem["source"], projectId=event["projectId"])
            targetItem["schema"] = sourceDsItem["schema"]
            put_dynamodb_item(table_name=shareItem["target"], item=targetItem)
        #updatedasetindex#

    
    return {}
