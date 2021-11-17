import redis
import json

r = redis.StrictRedis(host='pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn', port=6379, db=1)


def codeTrue():
    return {
            "status": "True",
            "message": "Code correct"
        }


def codeFalse():
    return {
        "status": "False",
        "message": "Code false"
    }


def lambdaHandler(event, context):  # 主函数入口
    status_code = 200
    try:
        event = event['body']
        if type(event) == str:
            event = json.loads(event)
        # r.setex(event["email"], value=int(event["code"]), time=3000)
        code = int(r.get(event["email"]))
        code_status = str(bool(code == int(event["code"])))  # 正确为True，错误为False
        code_choice = {"True": codeTrue, "False": codeFalse}
        result_message = code_choice[code_status]()

    except redis.exceptions.ConnectionError as e:
        result_message = {
                "status": "error",
                "message": "redis false:" + str(e)
            }
    except Exception as e:
        result_message = {
            "status": "error",
            "message": str(e)
        }
    if result_message["status"] == "error":
        status_code = 503

    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result_message)
    }
