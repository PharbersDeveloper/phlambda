'''
event = {
    "index": 0,
    "doneJobs": [],
    "fullfilled": false,
    "dags": [
        {
          "name": "compute_AlexOut",
          "parents": [],
          "children": []
        }
    ]
}

'''


import json
import boto3
from datetime import datetime
from collections import deque
from sms import *
from smsv2 import *


def lambda_handler(event, context):
    # result = event
    result = stageIterator(event["dags"], event["doneJobs"])
    sm = {}
    stack2smdefs(result["stack"], event, sm, 'StateMachineStartHook')
    s3 = boto3.client('s3')
    s3.put_object(
        Body=json.dumps(sm).encode(),
        Bucket='ph-max-auto',
        Key='2020-08-11/' + event['runnerId'] + "-step-" + str(event["index"]) + '.json'
    )
    result["index"] = event["index"] + 1
    result["args"] = event["args"]
    result["dags"] = event["dags"]
    result["sm"] = '2020-08-11/' + event['runnerId'] + "-step-" + str(event["index"]) + '.json'
    result["smarn"] = ""
    del result["stack"]
    return result


if __name__ == "__main__":
    with open("../events/event.json", "r") as read_file:
        event = json.load(read_file)
        lambda_handler(event, None)
