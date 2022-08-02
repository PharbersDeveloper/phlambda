import json
from datetime import datetime
#import boto3
#from boto3.dynamodb.conditions import Key
from puttonotification import put_notification
from pherrorlayer import *


#---- 处理抛出的错误信息 -----------#
def lambda_handler(event, context):
    print("*"*50 + " EVENT " + "*"*50)
    print(event)



    #dt = datetime.now()
    #ts = datetime.timestamp(dt)
    #put_notification(event['runnerId'], pid, None, 0, "", int(ts), event['owner'], event['showName'], status='running')

    return {}


