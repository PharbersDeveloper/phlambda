import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Attr,Key


'''
args = {
  "common": {
    "runnerId": "sample_sample_developer_2022-07-04T05:49:39+00:00",
    "projectId": "Dp10sMiAYXWxRZj",
    "projectName": "sample",
    "owner": "16dc4eb5-5ed3-4952-aaed-17b3cc5f638b",
    "showName": "赵浩博",
    "tenantId": "zudIcG_17yj8CEUoCTHg"
  },
  "calculate": {
    "type": "share",
    "name":"shareName",
    "share":[
      { "company":"",
       "sourceProjectId":"",
       "datasetName":"",
       "version":""}
],
    "recursive": true
  },
  "engine": {
    "type": "awsemr",
    "id": "j-XVHN3AUBDOMH",
    "dss": {
      "ip": "192.168.16.93"
    }
  }
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
            'date': str(datetime.now().timestamp()),
            'owner': owner,
            'projectId': projectId,
        }
    )
    print(response)


def lambda_handler(event, context):
    print(event)

    for shareItem in event["calculate"]["share"]:
        #---- query item of dataset -----------#
        datasetItem = get_ds_with_index(dsName=shareItem["datasetName"], projectId=shareItem["sourceProjectId"])

        versionId =shareItem["sourceProjectId"] + "_" + datasetItem["id"]
        #----- update version -------------------#
        put_to_version(id=versionId, name=shareItem["version"], datasetId=datasetItem["id"], owner=event["common"]["owner"], projectId=shareItem["sourceProjectId"])

    #----- update version -------------------#


    return {}
