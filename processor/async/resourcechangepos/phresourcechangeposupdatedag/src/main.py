import json
import math
import random
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
'''
args:
    event = {
        "traceId": "traceId",
        "projectId": "projectId",
        "projectName": "projectName",
        "owner": "owner",
        "showName": "showName",
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
                }
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
        script: {
            "old": {
                "name": compute_A,
                "id": "22jpN8YtMIhGTnW"
            },
            "new": {
                "name": "compute_B",
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
'''


def generate():
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
              "abcdefghijklmnopqrstuvwxyz" \
              "0123456789"
    charsetLength = len(charset)
    keyLength = 3 * 5
    array = []
    for i in range(keyLength):
        array.append(charset[math.floor(random.random() * charsetLength)])

    return "".join(array)


def create_link_item(projectId, sortVersion, cat, cmessage, ctype, flowVersion, level, name, position, prop, representId,
                 runtime, traceId):

    Item = {
        "projectId": projectId,
        "sortVersion": sortVersion,
        "cat": cat,
        "cmessage": cmessage,
        "ctype": ctype,
        "flowVersion": flowVersion,
        "level": level,
        "name": name,
        "position": position,
        "prop": prop,
        "representId": representId,
        "runtime": runtime,
        "traceId": traceId
    }

    return Item


def get_all_item_from_dag(projectId):
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        KeyConditionExpression=Key("projectId").eq(projectId)
    )
    return res.get("Items")


def lambda_handler(event, context):
    print(event)
    # ???????????????project items
    all_dag_items = get_all_item_from_dag(event["projectId"])
    all_link_dag_items = list(item for item in all_dag_items if item["ctype"] == "link")
    # ??????????????????dataset???inputs
    deleteLinkItems = []
    insertLinkItems = []

    # ??????????????????ds
    old_input_ds_names = list(old_ds["name"] for old_ds in event["datasets"]["inputs"]["old"])
    # ??????????????????ds
    new_input_ds_names = list(new_ds["name"] for new_ds in event["datasets"]["inputs"]["new"])
    # ??????????????????ds
    old_output_ds_name = event["datasets"]["output"]["old"]["name"]
    # ??????????????????ds
    new_output_ds_name = event["datasets"]["output"]["new"]["name"]

    # ?????????name?????????link
    # ??????cmessage??????script id???????????????
    job_id = event["script"]["old"]["id"]
    deleteLinkItems = list(item for item in all_link_dag_items if json.loads(item["cmessage"])["sourceId"] == job_id or json.loads(item["cmessage"])["targetId"] == job_id)
    # ??????????????????link
    # ??????input???job link
    new_input_ds_msg = list({"name": item["name"], "representId": item["representId"]} for item in all_dag_items if item["name"] in new_input_ds_names)
    for input_ds_msg in new_input_ds_msg:
        input_link_represent_id = generate()
        cmessage = {
            "sourceId": input_ds_msg["representId"],
            "sourceName": input_ds_msg["name"],
            "targetId": job_id,
            "targetName": event["script"]["new"]["name"]
        }
        input_link = create_link_item(event["projectId"], "developer_" + input_link_represent_id, "", json.dumps(cmessage, ensure_ascii=False), "link", "developer",
                         "", "empty", "", "", input_link_represent_id, "", event["traceId"])
        insertLinkItems.append(input_link)

    # ??????job???output link
    new_output_ds_msg = list({"name": item["name"], "representId": item["representId"]} for item in all_dag_items if item["name"] == new_output_ds_name)[0]
    new_output_link_representId = generate()
    cmessage = {
        "sourceId": job_id,
        "sourceName": event["script"]["new"]["name"],
        "targetId": new_output_ds_msg["representId"],
        "targetName": new_output_ds_msg["name"]
    }
    new_output_link = create_link_item(event["projectId"], "developer_" + new_output_link_representId, "", json.dumps(cmessage, ensure_ascii=False), "link", "developer",
                                  "", "empty", "", "", new_output_link_representId, "", event["traceId"])
    insertLinkItems.append(new_output_link)

    # dag??????script?????????
    del_script_item = [item for item in all_dag_items if item["representId"] == event["script"]["old"]["id"]][0]
    deleteLinkItems.append(del_script_item)
    insert_script_item = del_script_item.copy()
    insert_script_item.update({
        "cmessage": event["script"]["new"]["name"],
        "name": event["script"]["new"]["name"],
        "traceId": event["traceId"]
    })
    insertLinkItems.append(insert_script_item)

    return {
        "deleteItems": deleteLinkItems,
        "insertItems": insertLinkItems
    }
