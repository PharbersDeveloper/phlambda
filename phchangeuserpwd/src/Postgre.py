import os
import psycopg2
os_env = os.environ
os_env['dbname'] = 'phplatform'
os_env['user'] = 'pharbers'
os_env['password'] = 'Abcde196125'
os_env['host'] = 'ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn'
os_env['port'] = '5432'


def SqlCall(sql):
    conn = psycopg2.connect(dbname=os_env['dbname'], user=os_env['user'], password=os_env['password'],
                            host=os_env['host'], port=os_env['port'])
    cur = conn.cursor()
    sql = sql
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows



