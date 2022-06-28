import os
import json
import boto3
import traceback
import datetime


'''
# cloud formation stack 创建与删除

'''


def lambda_handler(event, context):
    print(event)
    event["parameters"]["ClusterID"] = event["ClusterID"]
    return event["parameters"]
