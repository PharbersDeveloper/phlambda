import os
import psycopg2
import json
import time

conn = psycopg2.connect(dbname=os.environ['DBNAME'], user=os.environ['USER'], password=os.environ['PASSWORD'],
                        host=os.environ['HOST'], port=os.environ['PORT'])


def zero(event):
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    sql = "INSERT INTO account (id,password,phoneNumber,defaultRole,email,employer,created,modified) VALUES (ID,PASSWORD,PHONENUMBER,DEFAULTROLE,EMAIL,EMPLOYER,CREATED,MODIFIED)"
    sql = sql.replace("ID", event["id"])  # 必须字段 用户ID
    sql = sql.replace("PASSWORD", event["password"])  # 必须字段 用户密码
    sql = sql.replace("PHONENUMBER", event["phoneNumber"])  # 必须字段 用户手机号
    sql = sql.replace("DEFAULTROLE", event["defaultRole"])  # 必须字段 默认账号
    sql = sql.replace("EMAIL", event["email"])  # 必须字段 用户邮箱
    sql = sql.replace("EMPLOYER", "zudIcG_17yj8CEUoCTHg")
    sql = sql.replace("CREATED", localtime)
    sql = sql.replace("MODIFIED", localtime)
    # cur.execute(sql)
    # conn.commit()
    result_code = 200
    result_message = {
        "status": "ok",
        "data": {
            "message": "seccessfully register"
        }
    }
    return result_code, result_message


def ltZero(event):
    result_code = 500
    result_message = {
        "status": "error",
        "data": {
            "message": "this account alread register"
        }
    }
    return result_code, result_message


def errorStatus(e):
    return {
        "statusCode": 500,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps({"status": "error",
                            "data": {
                                "message": str(e)
                            }})
    }


def lambdaHandler(event, context):
    # 数据库全部字段id,name,wechatOpenId,password,phoneNumber,defaultRole,email,employer,created,modified,firstName,lastName,picture,notification
    try:
        event = json.loads(event['body'])
        sql = "SELECT id FROM account WHERE email = '{}'".format(event['email'])
        cur = conn.cursor()
        cur.execute(sql)
        rows = str(len(cur.fetchall()))
        number_choice = {"0": zero, "1": ltZero}
        result_code, result_message = number_choice[rows](event)
    except psycopg2.OperationalError as e:
        return errorStatus(e)
    except KeyError as e:
        return errorStatus(e)
    except Exception as e:
        return errorStatus(e)
    else:
        return {
            "statusCode": result_code,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(result_message)
        }
