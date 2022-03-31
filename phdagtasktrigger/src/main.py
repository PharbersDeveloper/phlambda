import requests
import json
import boto3
from handleeventmessage import HandleTaskMessage
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
import time
import os

# ssm get url

def get_ssm_dict():
    client = boto3.client('ssm')
    response = client.get_parameter(
        Name='airflow_args'
    )
    ssm_dict = json.loads(response.get("Parameter").get("Value"))
    return ssm_dict

format_args = {"project_name":"demo","flow_version":"developer","run_id":"demo_demo_developer_2022-03-28T03:27:44+00:00","task_id":"demo_demo_developer_compute_B","clean_cat":"self_only"}

def process_insert_event(event):
    # 获取新插入item的 partition_key, sort_key, message
    item_list = []
    records = event.get("Records")
    for record in records:
        if record.get("eventName") == "INSERT":
            new_image = record["dynamodb"]["NewImage"]
            item = {}
            for item_key in list(new_image.keys()):
                value = new_image[item_key]
                item_value = list(value.keys())[0]
                item[item_key] = value[item_value]
            item_list.append(item)

    return item_list

def handle_key_and_value(input_dict,key,value):
    try:
        import re
        original_str = str(input_dict)
        patter_rule = f"[\"\']{key}[\"\']:\s+?.'S':\s+?[\"\']{value}[\"\'].,"
        match_result = re.findall(pattern=patter_rule, string=original_str)
        if len(match_result) == 0:
            message = f"key: {key} or value: {value} not exist !"
            status = False
        else:
            message = f"key: {key} and value: {value} is ok, match_result is: {match_result}"
            status = True
    except Exception as e:
        message = str(e)
        status = False
    print(message)
    return status, message

def insert_action(event, operate_type):
    try:
        dynamodb = DynamoDB()
        data = {
            "table_name": "notification"
        }
        tmp_msg = {"type": "operation", "opname": "35cca7e1-45d9-4a6e-80f6-09e5417feb33", "opgroup": "-1",
                   "cnotification": {"status": "remove_Job_succeed", "data": "{}", "error": "{}"}}
        item = {}
        message = {}
        message.update({"projectId": event.get("projectId")})
        message.update({"projectName": event.get("projectName")})
        item.update({"id": GenerateID().generate()})
        item.update({"date": str(int(round(time.time() * 1000)))})
        item.update({"projectId": event.get("projectId")})
        item.update({"code": 0})
        item.update({"showName": event.get("showName")})
        item.update({"jobDesc": "created"})
        item.update({"comments": ""})
        item.update({"owner": event.get("owner")})
        item.update({"message": json.dumps(tmp_msg,  ensure_ascii=False)})
        item.update({"jobCat": operate_type})
        data.update({"item": item})
        dynamodb.putData(data)
        exec_info = "insert action success"
    except Exception as e:
        exec_info = str(e)
    return exec_info

# 运行指定dag
def lambda_handler(event, context):

    event = json.loads(event.get("Records")[0].get("body"))
    jobcat_value = os.getenv("JOBCAT_VALUE")
    status, status_message = handle_key_and_value(event,'jobCat', jobcat_value)
    if status == True:
        item_event = process_insert_event(event)
        item_event[0]['message'] = format_args
        msg = item_event[0]['message']
        ssm_dict = get_ssm_dict()

        res = HandleTaskMessage(ssm_dict, msg).handle_retry_process()
        insert_action(msg, str(jobcat_value))

        return {
            "headers": {"Access-Control-Allow-Origin": "*"},
            "statusCode": 200 if res["status"] == "success" else 502,
            "body": json.dumps(res)
        }
    else:
        print(status_message)