import json
import boto3
from boto3.dynamodb.conditions import Attr, Key
import traceback


'''
通过参数，删除所有的steps
args = {
    "stackNames.$": "$.iterator.stackNames"
}
'''

client = boto3.client('cloudformation')


def lambda_handler(event, context):
    stackNames = event["stackNames"]

    while len(stackNames) == 0:
        curSn = stackNames[0]
        stackNames = stackNames[1:]
        
        try:
            response = client.describe_stacks(
                StackName=sn
            )
            print(response)
            return {
               "stackNames": stackNames,
                "wait": True
            }
        except:
            traceback.print_exc()
          
    return {
        "stackNames": [],
        "wait": False
    }  
