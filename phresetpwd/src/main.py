import os
import psycopg2
import json


def resultTrue():
    return {
        "status": "ok",
        "data": {
            "message": "change password success"
        }
    }


def resultFalse():
    return {
        "status": "ok",
        "data": {
            "message": "change password failure"
        }
    }


def lambdaHandler(event, context):
    statusCode = 200
    try:
        conn = psycopg2.connect(dbname=os.environ['DBNAME'], user=os.environ['USER'], password=os.environ['PASSWORD'],
                                host=os.environ['HOST'], port=os.environ['PORT'])
        event = json.loads(event['body'])
        sql = "UPDATE account SET password='{}' WHERE email = '{}'".format(event['password'], event['email'])
        cur = conn.cursor()
        cur.execute(sql)
        judge_result = {"True": resultTrue, "False": resultFalse}
        result_message = judge_result[str(bool(cur.rowcount))]()
        conn.commit()
    except psycopg2.ProgrammingError as e:
        result_message = {
            "status": "error",
            "data": {
                "message": "database failure:" + str(e)
            }
        }
    except psycopg2.OperationalError as e:
        result_message = {
            "status": "error",
            "data": {
                "message": "connect database failure:" + str(e)
            }
        }
    except Exception as e:
        result_message = {
            "status": "error",
            "data": {
                "message": str(e)
            }
        }
    if result_message["status"] == "error":
        statusCode = 503
    return {
        "statusCode": statusCode,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        },
        "body": json.dumps(result_message)
    }
