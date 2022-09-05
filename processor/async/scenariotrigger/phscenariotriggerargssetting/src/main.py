import json
import time
import boto3
from boto3.dynamodb.conditions import Key


'''
通过scenarioSteps 创建每个step的pharbers-trigger参数
并返回triggerSteps
args:
    event = {
            "projectId": "ggjpDje0HUC2JW",
            "tenantId": "zudIcG_17yj8CEUoCTHg",
            "projectName": "demo",
            "owner": "alfred",
            "showName": "alfred",
            "tenantInfo": {
                "engine": {
                  "ClusterID": "j-3FFGAYRYQ8UN2",
                  "ClusterDNS": "ec2-69-230-249-153.cn-northwest-1.compute.amazonaws.com.cn"
                },
                "olap": {
                  "PrivateIp": "192.168.35.250",
                  "PublicIp": "161.189.42.22",
                  "PrivateDns": "ip-192-168-35-250.cn-northwest-1.compute.internal",
                  "PublicDns": "ec2-161-189-42-22.cn-northwest-1.compute.amazonaws.com.cn"
                }
            },
            "scenarioStep": {
                "detail": {
                    "type": "dataset",
                    "recursive": false, 
                    "ignore-error": false, 
                    "name": "1235"
                },
                'confData': {}
            }
        }

return:
        {
            "common": {
                "traceId": "autoweight_autoweight_developer_2022-06-01T01:54:08+00:00",
                "runnerId": "autoweight_autoweight_developer_2022-06-01T01:54:08+00:00",
                "projectId": "xu68bxmMFJo6-o9",
                "projectName": "autoweight",
                "owner": "16dc4eb5-5ed3-4952-aaed-17b3cc5f638b",
                "showName": "赵浩博",
                "tenantId": "zudIcG_17yj8CEUoCTHg"
            },
            "action": {
                "cat": "runDag",
                "desc": "runDag",
                "comments": "something need to say",
                "message": "{\"optionName\":\"run_dag\",\"cat\":\"intermediate\",\"actionName\":\"weight_data_target (autoweight_autoweight_developer_2022-06-01T01:54:08+00:00)\"}",
                "required": true
            },
            "calculate": {
                "type": "dataset",
                "name": "weight_data_target",
                "conf": {
                    "datasets": [
                        {
                            "name": "mkt_mapping",
                            "representId": "QZwGeezIODKYA2H",
                            "version": [],
                            "cat": "catalog",
                            "prop": {
                                "path": "",
                                "partitions": 1,
                                "format": "",
                                "tableName": "mkt_mapping",
                                "databaseName": "zudIcG_17yj8CEUoCTHg"
                            }
                        },
                        {...}
                    ],
                    "scripts": [],
                    "userConf": {},
                    "ownerId": "16dc4eb5-5ed3-4952-aaed-17b3cc5f638b",
                    "showName": "赵浩博",
                    "jobDesc": "runDag1654047907372"
                },
                "recursive": false
                },
            "engine": {
                "type": "awsemr",
                "id": "j-PX68RDFOX82D",
                "dss": {
                    "ip": "192.168.55.39"
                }
            }
        }
        
'''

dynamodb = boto3.resource('dynamodb')


def get_scenario_step(scenarioId, id):
    ds_table = dynamodb.Table('scenario_step')
    res = ds_table.query(
        KeyConditionExpression=Key("scenarioId").eq(scenarioId) & Key("id").eq(id)
    )
    return res.get("Items")[0]


def get_scenario(projectId, id):
    ds_table = dynamodb.Table('scenario')
    res = ds_table.query(
        KeyConditionExpression=Key("projectId").eq(projectId) & Key("id").eq(id)
    )
    return res.get("Items")[0]


def lambda_handler(event, context):
    print(event)
    projectId = event.get("projectId")
    scenarioId = event.get("scenarioId")
    CodeFree = event.get("CodeFree")
    confData = json.loads(event.get("confData"))
    scenario_args: list = json.loads(get_scenario(projectId, scenarioId).get("args"))
    for key, value in confData.items():
        name = value[value.rfind("$"):]
        value = CodeFree.get("name", "")
        if not value:
            value = [arg.get("default", "") for arg in scenario_args if arg.get("name") == name]
        confData[key] = value[0] if value else ""
    return confData
