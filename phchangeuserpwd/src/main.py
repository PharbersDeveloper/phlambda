import os
import psycopg2

os_env = os.environ
# os_env['DBNAME'] = 'phplatform'
# os_env['USER'] = 'pharbers'
# os_env['PASSWORD'] = 'Abcde196125'
# os_env['HOST'] = 'ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn'
# os_env['PORT'] = '5432'


def sqlCall(sql):
    conn = psycopg2.connect(dbname=os_env['DBNAME'], user=os_env['USER'], password=os_env['PASSWORD'],
                            host=os_env['HOST'], port=os_env['PORT'])
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


def reword_sql(sql):
    conn = psycopg2.connect(dbname=os_env['DBNAME'], user=os_env['USER'], password=os_env['PASSWORD'],
                            host=os_env['HOST'], port=os_env['PORT'])
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def Re_Passwords(id, password, new_password):
    if len(sqlCall("select id from account where id='{}'".format(id))) == 0:
        return '账户不正确'
    elif len(sqlCall("select id from account where id='{}' and password='{}'".format(id, password))) == 0:
        return "密码不正确"
    else:
        sql = "UPDATE account SET password = '{}' WHERE id = '{}'".format(new_password, id)
        reword_sql(sql)
        return "密码修改成功"


def Run(event, context):
    result_str = Re_Passwords(event['id'], event['password'], event['new_password'])
    return result_str


# if __name__ == "__main__":
#     import json
#
#     with open("../events/event.json", 'r') as f:
#         data = json.load(f)
#     data = json.loads(data['body'])
#     # data['id'] = 'fdasfds'
#     data['password'] = 'fsdafdsfsad'
#     data['new_password'] = '1cd7fc9d631b3541354d5119236bae5f668e02e7c9472d9f0f56f83ccf2bc582'
#     print(Run(data, ''))
