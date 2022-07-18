import json
import os
import boto3
from clickhouse_driver import Client
from boto3.dynamodb.conditions import Key

'''
args = {
    "common": {
        "projectId": "ZyQpzttbwmvQcCf",
        "projectName": "pchc_mapping",
        "tenantId": "zudIcG_17yj8CEUoCTHg",
        "datasetName": "I6FDBI62N9VLus4"
    },
    "mappings": [
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
        self.Mappings = event["mappings"]
        self.result = {}
        self.statusCode = 200

    def get_tableName(self):
        return self.event["common"]["projectId"] + "_" + self.event["common"]["datasetName"]

    def Get_Ip_of_loap(self, tenantId):
        resource = self.get_dict_ssm_parameter(tenantId)
        PublicDns = resource["olap"]["PrivateIp"]
        return PublicDns

    def MakeSingleColConvertSqlExpress(self, tableName, colName, dataType):

        SingleSqlExpress = f"ALTER TABLE `{tableName}` MODIFY COLUMN  `{colName}` `{dataType}`;"
        return SingleSqlExpress

    def GetClickHouseClient(self, *args, **kwargs):
        ckClient = Client(*args, **kwargs)
        return ckClient

    def get_dict_ssm_parameter(self, parameter_name):
        ssm_client = boto3.client('ssm')
        response = ssm_client.get_parameter(
            Name=parameter_name,
        )
        print(response)
        value = json.loads(response["Parameter"]["Value"])

        return value

    def get_ds_with_index(self, dsName, projectId):

        dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")
        ds_table = dynamodb_resource.Table('dataset')
        res = ds_table.query(
            IndexName='dataset-projectId-name-index',
            KeyConditionExpression=Key("projectId").eq(projectId)
                                   & Key("name").begins_with(dsName)
        )
        return res["Items"][0]

    #--------------检查表名是否存在-------------------#
    def CheckTableExist(self, client, dataBase, tableName):
        allTableNames = client.execute(f"SELECT DISTINCT table FROM system.columns WHERE database='{dataBase}';")
        allTableNames = list(map(lambda x: x[0], allTableNames))
        if tableName not in allTableNames:
            raise Exception(f"{tableName} not in exist in database of {dataBase}.")

    def put_dynamodb_item(self, table_name, item):

        dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")
        table = dynamodb_resource.Table(table_name)
        resp = table.put_item(
            Item=item
        )
        print("*"*50+"put  item to dataset" + "*"*50)
        print(item)

    def ConverSchemaOfDataType(self, dyName, OldItem,colItem):

        Originalschema = json.loads(OldItem["schema"]) if isinstance(OldItem["schema"], str) else OldItem["schema"]
        print("*"*50+"original schema " + "*"*50)
        print(Originalschema)
        for elem in Originalschema:
            if elem["src"] == colItem["column"]:
                elem["type"] = colItem["to"]

        OldItem["schema"] = Originalschema if isinstance(Originalschema, str) else json.dumps(Originalschema, ensure_ascii=False)
        print("*"*50+"now schema " + "*"*50)
        print(OldItem["schema"])
        #-- put item to ds --#
        self.put_dynamodb_item(table_name=dyName, item=OldItem)

    def IsDBException(self, stringOfError):
        import re
        error_pattern = "DB::Exception"
        match_result = re.findall(pattern=error_pattern, string=str(stringOfError))
        if len(match_result) > 0:
            return True
        else:
            return False

    def ConvertColumnsDataType(self):
        ip = self.Get_Ip_of_loap(self.event["common"]["tenantId"])
        ckClient = self.GetClickHouseClient(host=ip, port=os.environ["CLICKHOUSE_PORT"])
        database = os.environ["CLICKHOUSE_DB"]
        #----- check table exist ------------------------------------#
        self.CheckTableExist(ckClient, database, self.get_tableName())
        ckClient.execute(f"use {database}; ")
        for colItem in self.Mappings:
            colName = colItem["column"]
            ConvertType = colItem["to"]
            OriginalType = colItem["from"]

            OldItem = self.get_ds_with_index(dsName=self.event["common"]["datasetName"], projectId=self.event["common"]["projectId"])

            try:
                SingleExcuteSql = self.MakeSingleColConvertSqlExpress(tableName=self.get_tableName(), colName=colName, dataType=ConvertType)
                ckClient.execute(SingleExcuteSql)
                #----- 更新dataset schema --------#
                self.ConverSchemaOfDataType(dyName="dataset", OldItem=OldItem, colItem=colItem)
                self.result["status"] = "success"
                self.result["message"] = f"{colName}: {OriginalType}  convert to {ConvertType} success"
            except Exception as e:
                #---- 还原dataset schema --------#
                #TODO 还原sql可能会引入新的异常
                print("*"*50 + " 回滚 " + "*"*50)
                try:
                    RestoreExcuteSql = self.MakeSingleColConvertSqlExpress(tableName=self.get_tableName(), colName=colName, dataType=OriginalType)
                    ckClient.execute(RestoreExcuteSql)
                    self.put_dynamodb_item(table_name="dataset", item=OldItem)
                    print("*"*50 + " 回滚成功 " + "*"*50)
                except Exception as RollBackError:
                    print("*"*50 + " 回滚失败 " + "*"*50)
                    print(str(RollBackError))

                print("*"*50 + "ERROR" + "*"*50 + "\n" + str(e))

                self.statusCode = 500
                self.result["status"] = "failed"
                self.result["message"] = f"{colName}: {OriginalType} can't convert to {ConvertType}"
                #raise Exception(f" {OriginalType} can't convert to {ConvertType}")


def lambda_handler(event, context):
    event = json.loads(event["body"])
    print("*"*50 + "Event" + "*"*50 + "\n", event)

    ConvertClient = ConvertDataTypesOfCache(event)
    ConvertClient.ConvertColumnsDataType()

    return {
        "statusCode": ConvertClient.statusCode,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(ConvertClient.result, ensure_ascii=False)
    }
