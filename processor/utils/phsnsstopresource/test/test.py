import json
import boto3
import requests
from boto3.dynamodb.conditions import Key, Attr

import boto3
import json

client = boto3.client('sns')

msg = {"test": "test"}

response = client.publish(
    TargetArn='arn:aws-cn:sns:cn-northwest-1:444603803904:CloudWatch_Stop_Resource_Topic',
    Message=json.dumps(msg),
)

print(response)

