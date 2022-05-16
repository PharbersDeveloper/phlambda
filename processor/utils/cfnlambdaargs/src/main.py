import os
import json
import boto3
import traceback
import datetime


'''
# cloud formation stack 创建与删除

args:
    event = {
        "iterator.$": "$.metadata.engine.iterator",
        "steps.$": "$.metadata.engine.steps"
    }

return:
    currentStep = {
        "steps"
    }
'''


def lambda_handler(event, context):
    print(event)
    return event["steps"][event["iterator"]]