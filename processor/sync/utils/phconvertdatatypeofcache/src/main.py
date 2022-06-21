import json
import boto3
from clickhouse_driver import Client

'''
args = {
    "common": {
        "projectId": "ZyQpzttbwmvQcCf",
        "projectName": "pchc_mapping",
        "tenantId": "zudIcG_17yj8CEUoCTHg",
        "datasetId": "I6FDBI62N9VLus4"
    },
    "Mappings": [
        {
            "column": "a",
            "from": "string",
            "to": "int"
        }
    ]
}
'''

class ConvertDataTypesOfCache:

    def __init__(self, event):
        self.event = event
        self.Mappings = event["Mappings"]

    def get_tableName(self):
        return self.event["common"]["projectId"] + "_" + self.event["common"]["datasetId"]

    def Get_Ip_of_loap(self, tenantId):
        resource = self.get_dict_ssm_parameter(tenantId)
        PublicDns = resource["olap"]["PublicDns"]
        return PublicDns

    def MakeSingleColConvertSqlExpress(self, tableName, colName, dataType):

        SingleSqlExpress = f"ALTER TABLE {tableName} MODIFY COLUMN {colName} {dataType};"
        return SingleSqlExpress

    def GetClickHouseClient(self, *args):
        ckClient = Client(*args)
        return ckClient

    def get_dict_ssm_parameter(self, parameter_name):
        ssm_client = boto3.client('ssm')
        response = ssm_client.get_parameter(
            Name=parameter_name,
        )
        print(response)
        value = json.loads(response["Parameter"]["Value"])

        return value

    def ConvertColumnsDataType(self):
        ip = self.Get_Ip_of_loap(self.event["common"]["tenantId"])
        ckClient = self.GetClickHouseClient(ip)
        database = "default"
        ckClient.execute(f"use {database}; ")
        for colItem in self.Mappings:
            colName = colItem["column"]
            ConvertType = colItem["to"]
            SingleExcuteSql = self.MakeSingleColConvertSqlExpress(tableName=self.get_tableName(), colName=colName, dataType=ConvertType)
            ckClient.execute(SingleExcuteSql)


def lambda_handler(event, context):

    result = {}
    try:
        ConvertClient = ConvertDataTypesOfCache(event)
        ConvertClient.ConvertColumnsDataType()
        statusCode = 200
        result["status"] = "success"
        result["message"] = "col convert success"
    except Exception as e:
        statusCode = 500
        result["status"] = "failed"
        result["message"] = str(e)

    return {
        "statusCode": statusCode,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result)
    }
