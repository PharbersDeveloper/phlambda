import os
import psycopg2
os_env = os.environ


def SqlCall(sql):
    conn = psycopg2.connect(dbname=os_env['DBNAME'], user=os_env['USER'], password=os_env['PASSWORD'],
                            host=os_env['HOST'], port=os_env['PORT'])
    cur = conn.cursor()
    sql = sql
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows



