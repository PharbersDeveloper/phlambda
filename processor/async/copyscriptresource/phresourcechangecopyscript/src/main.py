import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')
'''
将错误提取出来写入到notification中
args:
    event = {
                "projectId": "ggjpDje0HUC2JW",
                "traceId": "",
                "projectName": "demo",
                "owner": "alfred",
                "showName": "alfred",
                "errors": {
                }
            },
return:
    {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
    }
}
'''


def get_dagconf_item(projectId, jobId):
    dagconf_table = dynamodb.Table('dagconf')
    res = dagconf_table.query(
        IndexName='dagconf-projectId-id-indexd',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("id").eq(jobId)
    )

    return res.get("Items")[0]


def copy_s3_file(source_file_path, target_file_path):

    s3_resource = boto3.resource("s3", region_name='cn-northwest-1')
    source_bucket = "ph-platform"
    target_bucket = "ph-platform"
    copy_source = {
        'Bucket': source_bucket,
        'Key': source_file_path
    }
    s3_resource.meta.client.copy(copy_source, target_bucket, target_file_path)


def lambda_handler(event, context):
    print(event)
    script = event["script"]
    # 查询dag_conf item
    # 修改jobPath
    dagconfItem = get_dagconf_item(event["projectId"], event["script"]["old"]["id"])
    # 此时jobPath已经被修改 所以需要获取jobPath 把new name 替换成 old name
    newJobPath = dagconfItem.get("jobPath")
    oldJobPath = dagconfItem.get("jobPath").replace(script["new"]["name"], script["old"]["name"])
    # 需要将oldJobPath copy 至 newJobPath
    copy_s3_file(oldJobPath, newJobPath)
    return 1
