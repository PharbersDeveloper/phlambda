import json
import boto3
import re
from marshmallow_jsonapi import Schema, fields

class GetGlueTables:
    def __init__(self):
        self.client = boto3.client('glue', 'cn-northwest-1')
        self.filter_keys = ['Name', 'DatabaseName', 'Owner', 'CreateTime', 'UpdateTime', 'LastAccessTime', 'StorageDescriptor', 'PartitionKeys', 'Parameters']

    def filter_resonse(self, response):
        response = response['TableList']
        def remove_keys_with_filter_list(input_dict):
            output_dict = dict((key, value) for key, value in input_dict.items() if key in self.filter_keys)
            output_dict["StorageDescriptor"] = output_dict["StorageDescriptor"]["Location"]
            output_dict["id"] = response.index(input_dict)
            return output_dict
        response = list(map(lambda x: remove_keys_with_filter_list(x), response))
        return response

    def get_tables(self, database_name):
        try:
            response = self.client.get_tables(DatabaseName=database_name)
            response = Convert2JsonAPI(GlueTable, many=True).build().dumps(self.filter_resonse(response))
        except Exception as e:
            response = HandleErrorMessage().dumps({"error_code": 404,"error_message": str(e)})
        return response

class Convert2JsonAPI:

    def __init__(self, model, many=False):
        self.model = model

        def dasherize(text):
            return re.sub(r'([a-z])([A-Z])', r'\1-\2', text).lower()

        class BuildClass(Schema):
            id = fields.Integer(dump_only=True)

            class Meta:
                type_ = model.type
                inflect = dasherize

        self.mc = BuildClass(many=many)
        for filed in self.model.attributes.keys():
            self.mc.dump_fields[filed] = self.model.attributes[filed]
            self.mc.fields[filed] = self.model.attributes[filed]

    def build(self):
        return self.mc

class HandleErrorMessage(Schema):
    id = fields.Str(dump_only=True)
    error_code = fields.Integer()
    error_message = fields.String()
    class Meta:
        type_ = "error_info"

class GlueTable:
    type = "guletables"
    attributes = {
        'Name': fields.Str(required=True),
        'DatabaseName': fields.Str(),
        'Owner': fields.Str(),
        'CreateTime': fields.Str(),
        'UpdateTime': fields.Str(),
        'LastAccessTime': fields.Str(),
        'Retention': fields.Str(),
        'StorageDescriptor': fields.Str(),
        'PartitionKeys': fields.Str(),
        'TableType': fields.Str(),
        'Parameters': fields.Str(),
        'CreatedBy': fields.Str(),
        'IsRegisteredWithLakeFormation': fields.Str(),
        'CatalogId': fields.Str()
    }

def lambda_handler(event,context):

    database_name = json.loads(event["body"])["glue_database_name"]
    response = GetGlueTables().get_tables(database_name)
    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        'body': response,
    }



