import random
import boto3
import redis
import json
# import time
# import jwt

r = redis.StrictRedis(host='pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn', port=6379, db=1)


def redisSetCode(address):  # 生成六位随机数
    code = ''.join([str(random.randint(1, 9)) for i in range(6)])
    r.setex(address, value=code, time=300)
    return code


def errorMessage(e):
    result_code = 503
    result_message = {
        "status": "error",
        "data": {
            "message": json.dumps(str(e))
        }
    }
    return result_code, result_message


# def creat_token(email_address):
#     data = {
#         # 公共声明
#         "iat": int(time.time()),  # 生效时间
#         "exp": int(time.time()) + 300,  # 过期时间
#         'iss': 'https://www.accounts.pharbers.com:4200/resetPasswordPage/',  # 发布者url地址
#         # 私有声明
#         "data": {
#             "email": email_address
#         }
#     }
#     # jwt 加密 payload 加密数据 key加密签名的钥匙 algorithm 用什么方法加密
#     jwt_encode = jwt.encode(payload=data, key='123456', algorithm='HS256')
#     return jwt_encode


def lambdaHandler(event, context):  # 主函数入口
    result_code = 200
    result_message = {}
    try:
        event = json.loads(event["body"])
        for address in event["target_address"]:
            code = redisSetCode(address)
            # url_tokens = 'https://www.accounts.pharbers.com:4200/resetPasswordPage/' + "?token=" + creat_token(address)  # 生成token加在url里
            events = {
                "body": json.dumps({
                    "address": address,
                    "code": code,
                    # "url_tokens": url_tokens,
                    "content_type": event["content_type"],
                    "subject": event["subject"],
                    "attachments": event["attachments"]
                })
            }

            lmd_client = boto3.client("lambda")
            response = lmd_client.invoke(  # 调用phemail发送邮件lambda函数
                FunctionName='lmd-phemail-V2',
                Payload=json.dumps(events).encode()
            )
        result_message = {
            "status": "ok",
            "data": {
                "message": "successfully send emails"
            }
        }
    except KeyError as e:
        result_code, result_message = errorMessage(e)
    except redis.exceptions.ConnectionError:
        e = "insert redis error"
        result_code, result_message = errorMessage(e)
    except Exception as e:
        result_code, result_message = errorMessage(e)
    return {
        "statusCode": result_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result_message)
    }
