import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
'''
这个函数只做一件事情，检查参数是否合法
args:
    event = {
        "common": {
            "traceId": "hbzhao-resource-change-position-traceId",
            "projectId": "Dp10sMiAYXWxRZj",
            "projectName": "code",
            "owner": "hbzhao-resource-change-position-owner",
            "showName": "hbzhao-resource-change-position-showName"
        },
        "action": {
            "cat": "changeResourcePosition",
            "desc": "change resource position",
            "comments": "something need to say",
            "message": "something need to say",
            "required": true
        },
        "notification": {
            "required": true      
        },
        "datasets": {
            "inputs": {
                "old": [{
                    "name": "A",
                    "cat": "uploaded"
                }],
                "new": [{
                    "name": "B",
                    "cat": "uploaded"
                }]
            },
            "output": {
                "old": {
                    "name": "A_out",
                    "cat": "intermediate"
                },
                "new": {
                    "name": "B_out",
                    "cat": "intermediate"
                }
            }
        },
        "script": {
            "old": {
                "name": "compute_A_out",
                "id": "22jpN8YtMIhGTnW"
            },
            "new": {
                "name": "compute_B_out",
                "runtime": "python",
                "inputs": "[\"B\"]",
                "output": "B_out"
            }
        }
    }
'''


def get_item_from_dag(name, projectId):
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        IndexName='dag-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").eq(name)
    )
    return res.get("Items")


def get_dag_conf_item_from_dynamodb(jobId, projectId):
    ds_table = dynamodb.Table('dagconf')
    res = ds_table.query(
        IndexName='dagconf-projectId-id-indexd',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("id").eq(jobId)
    )
    return res.get("Items")


def check_parameter(event):

    # 1. common 必须存在
    if not event.get("common"):
        raise Exception('common must exist')

    # 2. action 必须存在cat 必须是 scenarioTrigger
    if not event.get("action"):
        raise Exception('action must exist')

    if not event["action"].get("cat") == "changeResourcePosition":
        raise Exception('action.cat must be changeResourcePosition')

    if not event.get("step") and not isinstance(event.get("step"), dict):
        raise Exception('step error')

    # 3. datasets 中的 old["name"] 必须在dag中查询到
    # 3. datasets 中的 new["name"] 必须在dag中查询到
    for old_dag in event["datasets"]["inputs"]["old"]:
        old_dag_name = old_dag["name"]
        old_dag_item = get_item_from_dag(old_dag_name, event["common"]["projectId"])
        if len(old_dag_item) == 0:
            raise Exception(f'{old_dag_name} item must exist')
    for old_dag in event["datasets"]["inputs"]["new"]:
        new_dag_name = old_dag["name"]
        new_dag_item = get_item_from_dag(new_dag_name, event["common"]["projectId"])
        if len(new_dag_item) == 0:
            raise Exception(f'{new_dag_name} item must exist')
    old_output_dag_name = event["datasets"]["output"]["old"]["name"]
    old_output_dag_item = get_item_from_dag(old_output_dag_name, event["common"]["projectId"])
    if len(old_output_dag_item) == 0:
        raise Exception(f'{old_output_dag_name} item must exist')
    new_output_dag_name = event["datasets"]["output"]["new"]["name"]
    new_output_dag_item = get_item_from_dag(new_output_dag_name, event["common"]["projectId"])
    if len(new_output_dag_item) == 0:
        raise Exception(f'{new_output_dag_name} item must exist')

    # 4. script中的 old id必须在dagconf表查询到
    dagconf_item = get_dag_conf_item_from_dynamodb(event["script"]["old"]["id"], event["common"]["projectId"])
    if len(dagconf_item) == 0:
        raise Exception('script item must exist')


    return True


def lambda_handler(event, context):
    print(event)
    return check_parameter(event)
    # 1. common 必须存在
    # 2. action 必须存在 cat 必须是 changeResourcePosition
    # 3. datasets 中的 old["name"] 必须在dag中查询到
    # 4. script中的 old id必须在dagconf表查询到
