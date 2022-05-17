from datetime import datetime
import boto3
import re

class AddVersionRecord:

    def __init__(self,database_of_glue):
        self.database_of_glue = database_of_glue
        self.current_time = str(datetime.now().timestamp())
        self.owner = "pharbers"
        self.glue_client = boto3.client('glue', 'cn-northwest-1')
        self.dynamodb_client = boto3.client('dynamodb', 'cn-northwest-1')
        self.dynamodb_table = "version"

    def parse_tablename_of_glue_database(self):
        response = self.glue_client.get_tables(DatabaseName=self.database_of_glue)
        tables = list(map(lambda x: x['Name'], response['TableList']))
        return tables

    def parse_version_of_glue_table(self, table_of_glue):
        response = self.glue_client.get_partitions(
            DatabaseName=self.database_of_glue,
            TableName=table_of_glue,
            #ExcludeColumnSchema=True|False,
        )
        version = list(map(lambda x: re.findall(r'version=(.*?)/',str(x['StorageDescriptor']['Location']))[0], response['Partitions']))
        return version

    def insert_item_into_dynamodb_table(self):

        for table in self.parse_tablename_of_glue_database():
            versions = self.parse_version_of_glue_table(table)
            for version in versions:
                try:
                    message = f"正在写入 glue table: {table}  version:{version}"
                    print(message)
                    item = self.compose_item_of_dynamodb(table, version)
                    #--dynamodb 写入数据
                    self.put_item_of_dynamodb(self.dynamodb_table, item)
                except Exception as e:
                    message = f"{table} version: {version} 写入失败"
                    print(message)
                    print(f"error: {e}")

    def compose_item_of_dynamodb(self, table_name, version_name):
        item = {
            'id': {'S': self.database_of_glue + '_' + table_name},
            'name': {'S': str(version_name)},
            'datasetId': {'S': str(table_name)},
            'date': {'S': self.current_time},
            'owner': {'S': str(self.owner)},
            'projectId': {'S': str(self.database_of_glue)}
        }
        return item

    def put_item_of_dynamodb(self, table_of_dynamodb, item):
        respose = self.dynamodb_client.put_item(
            TableName=table_of_dynamodb,
            Item=item
        )
        return respose




