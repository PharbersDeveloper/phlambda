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


def status_itme(projectId, traceId, scenarioId):
    item = {
        "id": projectId,
        "startAt": str(int(round(time.time()*1000))),
        "scenarioId": scenarioId,
        "traceId": traceId,
        "endAt": "",
        "status": "running"
    }
    return item


def put_item(item):
    dynamodb_table = dynamodb.Table("scenario_status")
    response = dynamodb_table.put_item(
        Item=item
    )


def lambda_handler(event, context):
    print(event)
    put_item(status_itme(**event))
    return True
