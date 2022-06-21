import boto3
from functools import reduce

'''
删除所有的dynamodb中的step表的索引记录

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "scripts": [
            {
                "projectId": "RL8iefdfGuRfbuN",
                "operatorParameters": "",
                "actionName": "compute_C",
                "outputs": "C",
                "runtime": "topn",
                "showName": "鹏钱",
                "jobDisplayName": "Alex_Alex_developer_compute_C",
                "jobVersion": "developer",
                "prop": "",
                "jobId": "MWJTtgs2VBrMzMi",
                "projectName": "Alex",
                "jobPath": "2020-11-11/jobs/python/phcli/Alex_Alex_developer/Alex_Alex_developer_compute_C/phjob.py",
                "jobName": "developer_MWJTtgs2VBrMzMi_Alex_Alex_compute_C",
                "timeout": 1000,
                "dagName": "Alex",
                "labels": "",
                "jobShowName": "compute_C",
                "owner": "5UBSLZvV0w9zh7-lZQap",
                "flowVersion": "developer",
                "id": "MWJTtgs2VBrMzMi",
                "traceId": "7890ec3821a949a78ea67f93f6c9497c",
                "inputs": "[\"A\"]"
            }
        ]
    }
'''

dynamodb = boto3.client("dynamodb")


def dynamoData2EntityData(record):
    item = {}
    for field in list(record.keys()):
        value = record[field]
        v_k = list(value.keys())[0]
        item[field] = value[v_k]
    return item


def get_steps(pk):
    result = dynamodb.query(
        TableName="step",
        Limit=1000,
        ExpressionAttributeValues={
            ":pjName": {
                "S": pk
            },
        },
        KeyConditionExpression="pjName = :pjName",
    )["Items"]
    return list(map(dynamoData2EntityData, result))


def lambda_handler(event, context):
    runtimes = ["python3", "python", "pyspark", "r", "sparkr"]
    hit_scripts = list(filter(lambda item: item["runtime"].lower() not in runtimes, event["scripts"]))
    deletion_scripts = list(set(list(map(lambda item: f"""{item["projectId"]}_{item["projectName"]}_{item["dagName"]}_{item["jobVersion"]}_{item["jobShowName"]}""",
                                         hit_scripts))))

    if deletion_scripts:
        deletion_steps = list(map(lambda item: {
            "DeleteRequest": {
                "Key": {
                    "pjName": {
                        "S": item["pjName"]
                    },
                    "stepId": {
                        "S": item["stepId"]
                    }
                }
            }
        }, reduce(lambda pre, next: pre + next, list(map(get_steps, deletion_scripts)))))
        dynamodb.batch_write_item(
            RequestItems={
                "step": deletion_steps
            }
        )

    return True
