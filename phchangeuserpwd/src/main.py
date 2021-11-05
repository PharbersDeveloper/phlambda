import os
import psycopg2

os_env = os.environ


def sqlCall(sql):
    conn = psycopg2.connect(dbname=os_env['DBNAME'], user=os_env['USER'], password=os_env['PASSWORD'],
                            host=os_env['HOST'], port=os_env['PORT'])
    cur = conn.cursor()
    sql = sql
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


def Re_Passwords(id, password, new_password):
    if sqlCall("select id from account where id='{}'".format(id)) == []:
        return '账户不正确'
    elif sqlCall("select id from account where id='{}' and password='{}'".format(id, password)) == []:
        return "密码不正确"

    else:
        # sql = "UPDATE account SET password = '{}' WHERE id = '{}'".format(new_password, id)
        # sql_call(sql)
        return "密码修改成功"


def Run(event, context):
    number = Re_Passwords(event['id'], event['password'], event['new_password'])
    return number
