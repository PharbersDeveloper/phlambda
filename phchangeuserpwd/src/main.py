import os
import psycopg2
import json
os_env = os.environ
conn = psycopg2.connect(dbname=os_env['DBNAME'], user=os_env['USER'], password=os_env['PASSWORD'],
                        host=os_env['HOST'], port=os_env['PORT'])


def lambdaHandler(event, context):
    event = json.loads(event['body'])
    sql = "SELECT id FROM account WHERE id = '{}' AND password = '{}'".format(event['id'], event['password'])
    cur = conn.cursor()
    cur.execute(sql)
    rows = len(cur.fetchall())
    if rows == 0:
        return {
            "statusCode": 204,
            "body": json.dumps("repassword False")
        }
    else:
        sql = "UPDATE account SET password='{}' WHERE id = '{}' AND password = '{}'".format(event['new_password'], event['id'], event['password'])
        cur.execute(sql)
        conn.commit()
        return {
            "statusCode": 200,
            "body": json.dumps("repassword success")
        }

