import os
import json
import boto3
import traceback
import datetime
import pandas as pd
import requests
from clickhouse_driver import Client


'''
args =  {
    "common": {
        "projectId":"",
        "projectName":"",
        "tenantId":"",
        "datasetId":""
    },
    "Mappings": [
        {
            "column":"",
            "from": "string",
            "to": "number"
        }
    ]
}
'''
event = {
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


class ConvertDataTypesOfCache:

    def __init__(self, event):
        self.event = event

    def get_tableName(self):
        return self.event["common"]["projectId"] + "_" + self.event["common"]["datasetId"]

    def Get_Ip_of_loap(self):
        resource = self.get_dict_ssm_parameter(self.event["common"]["tenantId"])
        olap = resource["olap"]
        return olap

    def CreateCastSqlExpress(self):
        CastData = self.event["Mappings"]

        SqlExpress = "SELECT * FROM" + ",".join(list(map(lambda x: " CAST( " + x["column"] + "," + x["to"] + ")", CastData)))
        print(SqlExpress)
        return SqlExpress

    def GetClickHouseClient(self, *args):
        ckClient = Client(*args)
        return ckClient

    def ConvertSingleColumnTypeByHttpsInterface(self):
        olap = self.Get_Ip_of_loap()
        PrivateIp = olap["PrivateIp"]
        PublicIp = olap["PublicIp"]
        PrivateDns = olap["PrivateDns"]
        PublicDns = olap["PublicDns"]
        print(PrivateIp)

        clickclient = Client(host=PublicDns)
        a = clickclient.execute("show databases;")
        print(a)
        pass

    def get_dict_ssm_parameter(self, parameter_name):

        ssm_client = boto3.client('ssm', region_name='cn-northwest-1', aws_access_key_id='AKIAWPBDTVEANKEW2XNC',
                                  aws_secret_access_key='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')
        #ssm_client = boto3.client('ssm')
        response = ssm_client.get_parameter(
            Name=parameter_name,
        )
        print(response)
        value = json.loads(response["Parameter"]["Value"])

        return value

    def create_table(self, client,table_name, *args):

        from functools import reduce
        schema = list(args)
        schema = tuple(map(lambda x: str(x) + " "+"String",schema))
        schema = "(" + str(reduce(lambda x,y: x + "," + y,schema)) + ")"

        cmd_of_create_table = "create table if not exists" + " " + table_name + schema + "engine=MergeTree;"
        client.execute(cmd_of_create_table)
        return table_name

    def ConvertColumnDataTypeByCastFunction(self):
        host = "1.116.159.250"
        client = Client(host=host)
        databases = client.execute("show databases;")
        print(databases)
        client.execute("use default")
        self.create_table(client,"test__", 'a','b','c')
        a = client.execute("show tables;")
        print(a)
        client.execute("insert into test__(a,b,c) values",[{"a":"1","b":"1","c":"1"},{"a":"22","b":"22","c":"22"}])
        a = client.execute("select * from test__")
        print(a)
        a = client.execute("DESCRIBE TABLE test__")
        print(a)
        client.execute("ALTER TABLE test__ MODIFY COLUMN a int ")
        #sql = "ALTER TABLE [db].name  MODIFY COLUMN a int"
        a = client.execute("DESCRIBE TABLE test_")
        print(a)


    def MappingDataTypes(self):
        pass



def lambda_handler(event, context):
    ConvertClient = ConvertDataTypesOfCache(event)
    #ConvertClient.CreateCastSqlExpress()
    ConvertClient.ConvertColumnDataTypeByCastFunction()



    '''
    result = {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": json.dumps(event["result"], ensure_ascii=False),
            "error": {}
        }
    }
    
    '''
if __name__ == '__main__':
    lambda_handler(event, " ")
