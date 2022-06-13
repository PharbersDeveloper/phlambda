import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')

'''
将错误提取出来写入到notification中
args:
    args:
    event = {
        "traceId": "traceId",
        "projectId": "projectId",
        "projectName": "projectName",
        "owner": "owner",
        "showName": "showName",
        "script": {
            "old": {
                "name": compute_A_out,
                "id": "22jpN8YtMIhGTnW"
            },
            "new": {
                "name": "compute_B_out",
                "runtime": "python",
                "inputs": "[\"B\"]",
                "output": "B_out"
            }
        }   
    },
return:
    {
        "deleteItems":[
            {}
        ],
        "insertItems":[
            {}
        ]
    }
}
'''
def get_dagconf_item(projectId, jobId):
    dagconf_table = dynamodb.Table('dagconf')
    res = dagconf_table.query(
        IndexName='dagconf-projectId-id-indexd',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("jobId").eq(jobId)
    )

    return res.get("Items")


def lambda_handler(event, context):
    print(event)
    script = event["script"]
    # 查询dag_conf item
    # 修改jobName, actionName, inputs, jobDisplayName, jobPath, jobShowName, outputs, runtime, traceId
    dagconfItem = get_dagconf_item(event["projectId"], event["script"]["old"]["id"])
    newJobName = dagconfItem.get("jobName").replace(script["old"]["name"], script["new"]["name"])
    return 1
