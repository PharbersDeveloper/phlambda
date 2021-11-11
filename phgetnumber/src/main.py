import os
import json
import psycopg2
import boto3


def getDsCount():

    return 0


# 暂时不做
def getFlowCount(tableName, projectId):
    return 0


# 暂时不做
def getScriptCount():
    return 0


__func_dict = {
    "ds_count": getDsCount,
    # "flow_count": getFlowCount,
    # "script_count": getScriptCount
}


def lambda_handler(event, context):

    return {}
    # return {
    #     'statusCode': 200,
    #     'headers': {'Access-Control-Allow-Origin': '*'},
    #     'body': json.dumps(final_res, ensure_ascii=False)
    # }
