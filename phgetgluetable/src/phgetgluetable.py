import datetime
import json
import boto3

class GetGlueTables:
    def __init__(self):
        self.client = boto3.client('glue', 'cn-northwest-1')
        self.filter_keys = ['Name', 'DatabaseName', 'Owner', 'CreateTime', 'UpdateTime', 'LastAccessTime', 'StorageDescriptor', 'PartitionKeys', 'TableType']

    def filter_resonse(self, response):
        response = response['TableList']
        def remove_keys_with_filter_list(input_dict):
            output_dict = dict((key, value) for key, value in input_dict.items() if key in self.filter_keys)
            output_dict["StorageDescriptor"].pop("Columns")
            return output_dict
        response = list(map(lambda x: remove_keys_with_filter_list(x),response))
        return response

    def get_tables(self, database_name):
        try:
            statusCode = 200
            response = self.client.get_tables(DatabaseName=database_name)
            response = {
                'message': 'success',
                'TableLIst': self.filter_resonse(response),
            }
        except Exception as e:
            statusCode = 200
            response = {
                'message': 'error',
                'error_info': str(e),
                'TableList': [],
            }
        return statusCode, response


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime(r"%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

def lambda_handler(event,context):

    database_name = json.loads(event["body"])["glue_database_name"]

    statusCode, response = GetGlueTables().get_tables(database_name)

    return {
        'statusCode': statusCode,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        'body': json.dumps({
            'ResponseMetadata': json.dumps(response, cls=DateEncoder),
        })
    }


