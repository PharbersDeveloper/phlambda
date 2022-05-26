import json
import boto3
import traceback
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
client = boto3.client('cloudformation')
ssm = boto3.client('ssm')

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


def resourceCheck(resource):
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

    result = 0
    properties = json.loads(resource["properties"])
    for prop in properties:
        tmpsm = "-".join([resource["role"], prop["type"], resource["tenantId"]]).replace("_", "-").replace(":", "-").replace("+", "-")
        response = client.describe_stacks(StackName=tmpsm)["Stacks"]
        if len(response) == 0:
            print("{} is stoped".format(tmpsm))
            result |= 0
        elif len(response) == 1 and response[0]["StackStatus"] in ["CREATE_IN_PROGRESS", "UPDATE_IN_PROGRESS"]:
            print("{} is starting".format(tmpsm))
            result |=1
        elif len(response) == 1 and response[0]["StackStatus"] in ["CREATE_COMPLETE", "UPDATE_COMPLETE"]:
            print("{} is started".format(tmpsm))
            result |= 2
        elif len(response) == 1 and response[0]["StackStatus"] in ["DELETE_IN_PROGRESS"]:
            print("{} is stoping".format(tmpsm))
            result |= 4
        else:
            raise Exception("unexcept status ({}) for {}".format(response[0]["StackStatus"], tmpsm))

    return result


def ssmCheck(tenantId):
    '''
    @return: 
        0: stoped
        2: started
    '''
    result = 0
    name = tenantId.replace("=", "-")
    try: 
        response = client.get_parameter(
            Name=tenantId
        )
        print(response)
        result |= 2
    except:
        result |= 0
    finally:
        return result


def ssmQueryTraceId(tenantId):
    '''
    @return: traceId
    '''
    name = tenantId.replace("=", "-")    
    response = client.get_parameter(
        Name=tenantId
    )
    print(response)
    value = json.loads(response["Parameter"]["Value"])
    return value["traceId"]
    

def errorMessage(e):
    code = 503
    message = {
        "status": -99,
        "message": json.dumps(str(e)),
        "traceId": ""
    }
    return code, message


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print(event)
    code = 200
    status = 0
    result = {
        "status": -99,
        "message": "",
        "traceId": ""
    }
    try:

        table = dynamodb.Table('resource')
        res = table.query(
            KeyConditionExpression=Key("tenantId").eq(event["tenantId"]),
            FilterExpression=Attr("ownership").eq("shared")
        )
        resources = res["Items"]
        print(resources)

        statusCode = 0
        for item in resources:
            statusCode |= resourceCheck(item)

        statusCode |= ssmCheck(event["tenantId"])

        print(statusCode)
        if (statusCode & 4) != 0:
            result["status"] = 4
            result["message"] = "stoping"
        elif (statusCode & 2) != 0:
            result["status"] = 2
            result["message"] = "started"
            status = 2
            message = "started"
        elif (statusCode & 1) != 0:
            result["status"] = 1
            result["message"] = "starting"
        elif statusCode == 0:
            result["status"] = 0
            result["message"] = "stoped"
        else:
            raise Exception("unknown error")
    except Exception as e:
        # printing stack trace
        traceback.print_exc()
        code, result = errorMessage(e)
    finally:
        return {
            "statusCode": code,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
            },
            "body": json.dumps(result)
    }
