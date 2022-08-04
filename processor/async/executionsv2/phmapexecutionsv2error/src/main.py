import json
from datetime import datetime
from puttonotification import put_notification
from pherrorlayer import *
import re



def ChangeStrToDict(data):
    return json.loads(data) if isinstance(data, str) else data

def FindErrorKey(key):
    Patter = re.compile(pattern='error', flags=re.IGNORECASE)
    result = Patter.findall(string=key)
    return True if len(result) > 0 else False

def FindErrorCause(data):
    data = ChangeStrToDict(data)
    try:
        tag = ChangeStrToDict(data['Cause'])
        return tag
    except:
        return False

def SearchErrorType(error):
    keys = ChangeStrToDict(error).keys()
    keys = list(filter(lambda x: FindErrorKey(x) is True, keys))
    if len(keys) == 0:
        return None
    else:
        cause = list(filter(lambda x: FindErrorCause(error[x]) is not False, keys))
        cause = list(map(lambda x: FindErrorCause(error[x]), cause))
        if len(cause) == 0:
            return None
        return cause

def MapErrorType(cause):

    if cause is None:
        tmp = serialization(Errors)
    else:
        #--- 错误详情，用于解析映射用 -----#
        ErrorKeys = list(*map(lambda x: list(x.keys()), cause))
        if "ExecutionArn" in ErrorKeys:
            tmp = serialization(EMRError)
        #TODO 后续出现新的错误类型再添加
        else:
            tmp = serialization(Errors)
    return tmp


#---- 处理抛出的错误信息 -----------#
def lambda_handler(event, context):
    print("*"*50 + " EVENT " + "*"*50)
    print(event)

    error = event["error"]
    print("*"*50 + "传入的 ERROR 信息 " + "*"*50)
    print(error)

    try:
        cause = SearchErrorType(error)

        #---- 基于error信息映射pherrorlayer ----------#
        #TODO 目前对事件错误信息掌握不全，需要多次测试后再编写映射逻辑
        errorMessage = MapErrorType(cause)
    except Exception as e:
        print("*"*50 + " 代码解析错误" + "*"*50, str(e))
        errorMessage = serialization(Errors)

    #--- 错误信息写入notification表 -----------#
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    put_notification(runnerId=event['runnerId'], projectId=event['projectId'], category=None, code=0, comments='', date=int(ts),
                     owner=event['owner'], showName=event['showName'], errorMessage=errorMessage, jobCat='notification',
                     jobDesc='executionFailed', status='failed', dynamodb=None)

    return {}



