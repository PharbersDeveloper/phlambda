from phchangeuserpwd.src.Postgre import SqlCall as sql_call


def Re_Passwords(id, password, new_password):
    print(id, password, new_password)
    if sql_call("select id from account where id='{}'".format(id)) == []:
        return '账户不正确'
    elif sql_call("select id from account where id='{}' and password='{}'".format(id, password)) == []:
        return "密码不正确"

    else:
        # sql = "UPDATE account SET password = '{}' WHERE id = '{}'".format(new_password, id)
        # sql_call(sql)
        return "密码修改成功"
