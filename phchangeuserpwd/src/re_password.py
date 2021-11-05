import re
import hashlib
from phchangeuserpwd.src.Postgre import SqlCall as sql_call


def Re_Passwords(count, password, new_password):
    password_len = 8 > len(new_password) < 16
    re_register = re.search("[0-9]+", new_password)
    re_letter = re.search("[a-zA-Z]+", new_password)
    re_special = re.search("[~!@#$)%^&*(\-._=+]+", new_password)
    re_all = re.search("[^0-9a-zA-Z~!@#$%^&*.()\-_=+]+", new_password)
    password = hashlib.sha256(password.encode('utf8')).hexdigest()
    account_station = {}
    account_station['account_false'] = bool(sql_call("select id from account where email='{}'".format(count))) == False
    account_station['password_false'] = bool(sql_call("select id from account where email='{}' and password='{}'".format(count, password))) == False
    account_station['password_len_false'] = bool(password_len)
    account_station['password_only_format_false'] = bool(re_all)
    account_station['password_should_format_false'] = (re_register and re_letter and re_special) == None
    # if sum(account_station.values())==0:
    #     new_password = hashlib.sha256(new_password.encode('utf8')).hexdigest()
    #     sql = "UPDATE account SET password = '{}' WHERE email = '{}'".format(new_password, count)
    #     sql_call(.format(count))
    return account_station
