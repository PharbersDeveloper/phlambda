import json
import boto3
from boto3.dynamodb.conditions import Attr,Key
from decimal import Decimal

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
                  "ClusterID": "j-1YZ9KPDZOMM57",
                  "ClusterDNS": "ec2-161-189-52-21.cn-northwest-1.compute.amazonaws.com.cn"
                },
                "olap": {
                  "PrivateIp": "192.168.31.189",
                  "PublicIp": "52.83.49.104",
                  "PrivateDns": "ip-192-168-31-189.cn-northwest-1.compute.internal",
                  "PublicDns": "ec2-52-83-49-104.cn-northwest-1.compute.amazonaws.com.cn"
                }
            }
            "scenarioSteps": [
                {
                    "detail": {
                        "type": "dataset",
                        "recursive": false, 
                        "ignore-error": false, 
                        "name": "1235"
                    }
                }，
                {
                    ...
                }
            ]
        }

return:
        {
            "triggerSteps": [
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
            },
            {...},
            ]
        }
'''


def lambda_handler(event, context):

    return 1
