import json
import boto3
from boto3.dynamodb.conditions import Key

'''
这个函数 查询steps表 返回steps
args:
    event = { 
        "traceId": "alfred-resource-creation-traceId",
        "projectId": "ggjpDje0HUC2JW",
        "projectName": "demo",
        "flowVersion": "developer",
        "dagName": "demo",
        "owner": "hbzhao",
        "showName": "赵浩博",
        "script": {
            "jobName": "compute_测试ds",
        }
        "steps": [ // 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
            {
                "id": "alextest_demo_demo_developer_compute_十多个",
                "stepId": "1",
                "index": "1",
                "runtime": "prepare",
                "stepName": "Initial Filter On Value",
                "ctype": "FillEmptyWithValue",
                "groupIndex": 0,
                "groupName": "",
                "expressionsValue": "JSON",
                "expressions": {
                    "type": "FillEmptyWithValue",
                    "code": "pyspark",
                    "params": {
                        "columns": ["订单内件数"],
                        "value": "4"
                    }
                }
            },
        ],
        "oldImage": [
            // 这个地方特别需要注意，保存steps修改前数据库的样子
        ]
    }
'''

dynamodb = boto3.resource("dynamodb")


def query_steps(projectId, projectName, flowVersion, jobName, **kwargs):
    pjName = "_".join([projectId, projectName, projectName, flowVersion, jobName])
    print(pjName)
    table = dynamodb.Table("step")
    response = table.query(
        KeyConditionExpression=Key('pjName').eq(pjName),
    )
    return response.get("Items")


def lambda_handler(event, context):
    print(event)
    result = []
    for step in query_steps(**event):
        step["expressions"] = json.loads(step["expressions"])
        result.append(step)
    return result
