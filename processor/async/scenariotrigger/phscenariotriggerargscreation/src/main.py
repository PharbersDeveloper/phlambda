import json
import time
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

from phstatemachineselect.main import statemachine_select

dynamodb = boto3.resource('dynamodb')
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


def get_dags_by_projectId(projectId):
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        KeyConditionExpression=Key("projectId").eq(projectId)
    )
    return res.get("Items")


def create_trigger_datasets(select_res, dag_items):
    trigger_datasets = []
    selected_items = list(filter(lambda x: x['representId'] in select_res["selected"] and
                                           x['representId'] != select_res["calculate"]["represent-id"] and
                                           x["cat"] == "dataset", dag_items))
    for selected_item in selected_items:
        trigger_datasets.append({
            "name": selected_item["name"],
            "representId": selected_item["representId"],
            "version": [],
            "cat": selected_item["runtime"],
            "prop": json.loads(selected_item["prop"])
        })
    return trigger_datasets


def create_trigger_args(trigger_datasets, event):
    # 创建runnerId
    run_time = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.localtime())
    runnerId = "{}_{}_developer_{}".format(event["projectName"], event["projectName"], run_time)
    trigger_args = {}

    # trigger的common部分
    common = {}
    common["traceId"] = runnerId
    common["runnerId"] = runnerId
    common["projectId"] = event["projectId"]
    common["projectName"] = event["projectName"]
    common["owner"] = event["owner"]
    common["showName"] = event["showName"]
    common["tenantId"] = event["tenantId"]
    trigger_args["common"] = common

    # trigger的action部分
    action = {}
    action["cat"] = "runDag"
    action["desc"] = "runDag"
    action["comments"] = "something need to say"
    jobShowName = event["scenarioStep"]["detail"]["name"]
    message = {
        "optionName": "run_dag",
        "cat": "intermediate",
        "actionName": f"{jobShowName} ({runnerId})"
    }
    action["message"] = json.dumps(message, ensure_ascii=False)
    action["required"] = True
    trigger_args["action"] = action
    
    # trigger的calculate部分
    calculate = {"conf": {}}
    calculate["type"] = "dataset"
    calculate["name"] = jobShowName
    calculate["conf"]["datasets"] = trigger_datasets
    calculate["conf"]["scripts"] = []
    calculate["conf"]["userConf"] = event["scenarioStep"]["confData"]
    calculate["conf"]["ownerId"] = event["owner"]
    calculate["conf"]["showName"] = event["showName"]
    calculate["conf"]["jobDesc"] = "runDag" + str(int(round(time.time() * 1000)))
    calculate["recursive"] = False
    trigger_args["calculate"] = calculate

    # trigger的engine部分
    engine = { "dss": {} }
    engine["type"] = "awsemr"
    engine["id"] = event["tenantInfo"]['engine']["ClusterID"]
    engine["dss"]["ip"] = event["tenantInfo"]["olap"]["PrivateIp"]
    trigger_args["engine"] = engine

    return trigger_args


def lambda_handler(event, context):
    print(event)
    # 1 遍历dag表 取出所有相关item
    dag_items = get_dags_by_projectId(event["projectId"])
    # 2 执行statemachine select方法获取所有representId
    # 输入{"projectId":"2LWyqFPIIwCSZEV","projectName":"autorffactor2","element":{"job":{"name":"compute_randomforest_result","represent-id":"QygahUFX4wE2586"}}}:
    representId = [item["representId"] for item in dag_items if item["name"] == event["scenarioStep"]["detail"]["name"]]
    element = {
        "dataset": {
            "name": event["scenarioStep"]["detail"]["name"],
            "represent-id": representId[0]
        }
    }
    select_event = {
        "projectId": event["projectId"],
        "projectName": event["projectName"],
        "element": element
    }
    select_res = statemachine_select(select_event)
    # 3 从selected的 id中 从dag_items根据selected的id查询 item 在去除job item和当前dataset item 创建好 calculate下conf下datasets
    trigger_datasets = create_trigger_datasets(select_res, dag_items)
    # 3拼接好trigger参数
    trigger_args = create_trigger_args(trigger_datasets, event)

    return trigger_args
