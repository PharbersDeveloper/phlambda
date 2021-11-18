import os
import psycopg2
import json
import time
from src.util.GenerateID import GenerateID

os.environ['DBNAME'] = "phlatform"
os.environ['USER'] = "pharbers"
os.environ['PASSWORD'] = "Abcde196125"
# os.environ['HOST'] = "ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn"
os.environ['HOST'] = "localhost"
os.environ['PORT'] = "5432"
conn = psycopg2.connect(dbname=os.environ['DBNAME'], user=os.environ['USER'], password=os.environ['PASSWORD'],
                        host=os.environ['HOST'], port=os.environ['PORT'])
cur = conn.cursor()


def partnerSql(id, name, employer, created):
    sql = "INSERT INTO partner(id, name, employee, created, modified) SELECT 'ID','NAME','{EMPLOYEE}','CREATED','CREATED' " \
          "WHERE NOT EXISTS(SELECT name FROM partner WHERE name='NAME')"
    sql = sql.replace("ID", id)
    sql = sql.replace("NAME", name)
    sql = sql.replace("EMPLOYEE", employer)
    sql = sql.replace("CREATED", created)
    cur.execute(sql)
    result = bool(cur.rowcount)
    print(result)
    return result


def roleSql(id):
    sql = "update role set \"accountRole\" = \"accountRole\"||'{ID}' where id='ThhQTGXUcJwv8fd8I5oW'"
    sql = sql.replace("ID", id)
    cur.execute(sql)
    result = bool(cur.rowcount)
    print(result)
    return result


def accountSql(id, email, password, firstName, lastName, created, modified, defaultRole, employer):
    sql = "INSERT INTO account(id,email,password,\"firstName\",\"lastName\",created,modified,\"defaultRole\",employer)" \
          " SELECT '{id}','{email}','{password}','{firstName}','{lastName}','{created}','{modified}','{defaultRole}','{employer}'" \
          " WHERE NOT EXISTS(SELECT id FROM account WHERE email='{email}')"
    sql = sql.format(
        id=id,
        email=email,
        password=password,
        firstName=firstName,
        lastName=lastName,
        created=created,
        modified=modified,
        defaultRole=defaultRole,
        employer=employer
    )
    cur.execute(sql)
    result = bool(cur.rowcount)
    print(result)
    return result


def errorStatus(type, e):
    return {"status": "error",
            "data": {
                "message": type + str(e)
            }}


def lambdaHandler(event, context):
    # 数据库全部字段id,name,wechatOpenId,password,phoneNumber,defaultRole,email,employer,created,modified,firstName,lastName,picture,notification
    statusCode = 200
    try:
        if type(event["body"]) == str:
            event = json.loads(event["body"])
        getid = GenerateID()
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        name = event["tenant"]["name"]
        email = event["account"]["email"]
        password = event["account"]["password"]
        firstName = event["account"]["firstName"]
        lastName = event["account"]["lastName"]
        created = localtime
        modified = localtime
        defaultRole = "ThhQTGXUcJwv8fd8I5oW"
        tenant_id = getid.generate()
        account_id = getid.generate()
        partner_result = partnerSql(tenant_id, name, account_id, created)
        role_result = roleSql(account_id)
        account_result = accountSql(
            id=account_id,
            email=email,
            password=password,
            firstName=firstName,
            lastName=lastName,
            created=created,
            modified=modified,
            defaultRole=defaultRole,
            employer=tenant_id
        )
        if (partner_result and role_result and account_result):
            conn.commit()
            result = {"status": "ok",
                      "data": {
                          "message": "account creat success"
                      }}
        else:
            result = {"status": "failure",
                      "data": {
                          "message": "account creat failure"
                      }}
        print(result)
    except psycopg2.OperationalError as e:
        result = errorStatus("PostgreSqlError: ", e)
    except KeyError as e:
        result = errorStatus("KeyError: ", e)
    except Exception as e:
        result = errorStatus("OtherError: ", e)
    if result["status"] == "error":
        statusCode = 503
    return {
        "statusCode": statusCode,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }


if __name__ == "__main__":
    with open("../events/success_register.json") as f:
        event = json.load(f)
    print(lambdaHandler(event, " "))
