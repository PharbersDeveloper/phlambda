import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

'''
1. 看stack 在不在 
    1.1 stackname 的获取方法是 在dynamodb中找到resource 表中 tenantid 下的所有 ownership 为 shared 值的 
    1.2 对每一个值中的property 遍历，形成一个stackname 的数组
    1.3 stackname 的名字规则为  <role>-<property.type>-<tenantId>
    1.4 所有的stak 在cloud formation 中都不存在 算过，要不然报错，说哪一个 stack 指向的role 以及type 存在
       
2. ssm 是否存在，如果存在，报错，不能重复创建并提交管理员

event = {
    "tenantId": "12345"
}

return = {
    "status": Number [ 0: stoped , 1: starting , 2: started , 4: stoping ]
    "message": String
    "traceId": String
}
'''


def resourceCheck(resouce):
    '''
    check resouce stack name
    & operator
    @param resouce: check item
    @return: 
        0: stoped
        1: starting 
        2: started
        4: stoping
    '''
    pass


def ssmCheck():
    '''
    @return: 
        0: stoped
        2: started
    '''
    pass


def ssmQueryTraceId():
    '''
    @return: traceId
    '''
    pass


def errorMessage(e):
    code = 503
    message = {
        "status": "error",
        "data": {
            "message": json.dumps(str(e))
        }
    }
    return code, message


def lambda_handler(event, context):
    print(event)
    event = json.loads(event["body"])
    code = 200
    status = 0
    result = {
        ""
    }
    try:

        table = dynamodb.Table('resource')
        res = table.query(
            KeyConditionExpression=Key("tenantId").eq(tenantId),
            FilterExpression=Attr("ownership") == "shared"
        )
        resources = res["Items"]

        result = 0
        for item in resources:
            result |= resourceCheck(item)

        result |= ssmCheck()

        print(result)
        if (result & 4) not 0:
            status = 4
            message = "stoping"
        elif (result & 2) not 0:
            status = 2
            message = "started"
        elif (result & 1) not 0:
            status = 1
            message = "starting"
        elif result == 0:
            status = 0
            message = "stoped"
        else:
            status = -99
            message = "unknown error"
            raise Exception(message)
    except Exception as e:
        code, message = errorMessage(e)
    finally:
        return {
            "statusCode": code,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(message)
    }
