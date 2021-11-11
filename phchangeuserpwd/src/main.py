import os
import psycopg2
import json
os_env = os.environ
# os_env['DBNAME'] ="phplatform"
# os_env['USER'] ="pharbers"
# os_env['PASSWORD'] ="Abcde196125"
# os_env['HOST'] ="ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn"
# os_env['PORT'] ="5432"
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
            "statusCode": 200,
            "body": json.dumps("repassword False")
        }
    else:
        sql = "UPDATE account SET password='{}' WHERE id = '{}' AND password = '{}'".format(event['new_password'], event['id'], event['password'])
        cur.execute(sql)
        conn.commit()
        conn.close()
        return {
            "statusCode": 200,
            "body": json.dumps("repassword success")
        }
