import random
import redis
import json
import boto3


# 1. first thing is to connect db, we use redis as tmp store
r = redis.StrictRedis(host='pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn', port=6379, db=1)

def genVerficationCode(address):
    tmp = ''.join([str(random.randint(1, 9)) for i in range(6)])
    r.setex(address, value=tmp, time=3600)
    return tmp

def lambdaHandler(event, context):  # 主函数入口
    result_code = 200
    result_message = {}
    try:
        event = event['body']
        event = json.loads(event)
        for address in event['target_address']:
            code = genVerficationCode(address)
            payload = {
                "body": {
                    "address": address,
                    "content_type": event['content_type'],
                    "attachments": event['attachments'],
                    "subject": event['subject'],
                    "code": code
                }
            }

            lmd_client = boto3.client("lambda")
            response = lmd_client.invoke(
                FunctionName='lmd-phemail-V2',
                Payload=json.dumps(payload).encode()
            )

            result_message = {
                "status": "ok",
                "data": {
                    "message": "seccessfully send emails"
                }
            }

    except Exception as e:
        result_message = {
            "status": "error",
            "error": {
                "message": "Unknown Error"
            }
        }

    return {
        "statusCode": result_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result_message)
    }
