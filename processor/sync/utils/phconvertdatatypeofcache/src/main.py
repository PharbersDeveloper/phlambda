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
        self.Mappings = event["mappings"]

    def get_tableName(self):
        return self.event["common"]["projectId"] + "_" + self.event["common"]["datasetName"]

    def Get_Ip_of_loap(self, tenantId):
        resource = self.get_dict_ssm_parameter(tenantId)
        PublicDns = resource["olap"]["PrivateIp"]
        return PublicDns

    def MakeSingleColConvertSqlExpress(self, tableName, colName, dataType):

        SingleSqlExpress = f"ALTER TABLE {tableName} MODIFY COLUMN  `{colName}` Nullable({dataType});"
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
        table.put_item(
            Item=item
        )


    def ConverSchemaOfDataType(self, dyName, dsName, projectId,colItem):

        def converSchema(OriginalItem, colItem):
            try:
                OriginalItem["type"] == colItem["to"] if OriginalItem["src"] == colItem['column'] else OriginalItem["type"]
            except:
                OriginalItem = OriginalItem
            return OriginalItem

        #---查表---#
        ds_Item = self.get_ds_with_index(dsName=dsName, projectId=projectId)
        Originalschema = json.loads(ds_Item["schema"]) if isinstance(ds_Item["schema"], str) else ds_Item["schema"]
        Changescheam = list(map(lambda x: converSchema(x, colItem), Originalschema))
        ds_Item["schema"] = Changescheam if isinstance(Changescheam, str) else json.dumps(Changescheam)
        #-- put item to ds --#
        self.put_dynamodb_item(table_name=dyName, item=ds_Item)

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
            try:
                SingleExcuteSql = self.MakeSingleColConvertSqlExpress(tableName=self.get_tableName(), colName=colName, dataType=ConvertType)
                ckClient.execute(SingleExcuteSql)
                #----- 修改dataset schema --------#
                self.ConverSchemaOfDataType(dyName="dataset",dsName=self.event["common"]["datasetName"], projectId=self.event["common"]["projectId"], colItem=colItem)

            except Exception as e:
                #---- 回滚 ------------#
                SingleExcuteSql = self.MakeSingleColConvertSqlExpress(tableName=self.get_tableName(), colName=colName, dataType=colItem["from"])
                ckClient.execute(SingleExcuteSql)
                if self.IsDBException(str(e)):
                    raise Exception(f" {colItem['from']} can't convert to {ConvertType}")
                raise Exception(str(e))


def lambda_handler(event, context):
    event = json.loads(event["body"])

    result = {}
    try:
        ConvertClient = ConvertDataTypesOfCache(event)
        ConvertClient.ConvertColumnsDataType()
        statusCode = 200
        result["status"] = "success"
        result["message"] = "col convert success"
    except Exception as e:
        print("*"*50 + " ERROR " + "*"*50 + "\n" + str(e))
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
