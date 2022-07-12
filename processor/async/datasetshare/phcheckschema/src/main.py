import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Attr, Key


'''
args = {
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

def IsTheSameScheam(source, target):

    sourceCol = list(map(lambda x: x["src"], source))
    targetCol = list(map(lambda x: x["src"], target))
    if list(set(sourceCol) - set(targetCol)) == 0:
        return True
    else:
        return False

def lambda_handler(event, context):
    print(event)

    for shareItem in event["shares"]:

        #---- query item of dataset -----------#
        sourceDsItem = get_ds_with_index(dsName=shareItem["source"], projectId=event["projectId"])
        sourceSchema = json.loads(sourceDsItem["schema"]) if isinstance(sourceDsItem["schema"], str) else sourceDsItem["schema"]

        targetDsItem = get_ds_with_index(dsName=shareItem["target"], projectId=event["projectId"])
        targetSchema = json.loads(targetDsItem["schema"]) if isinstance(targetDsItem["schema"], str) else targetDsItem["schema"]

        if len(targetSchema) != 0:
            if IsTheSameScheam(sourceSchema, targetSchema) is False:
                raise Exception(f"The schema of  {shareItem['source']} and {shareItem['target']}  is not the same. "
                                f"detail: {shareItem['source']}: {sourceSchema}, {shareItem['target']}: {targetSchema}.")

    return True
