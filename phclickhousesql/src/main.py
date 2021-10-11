import boto3
import re
from functools import reduce
from clickhouse_driver import Client

client = boto3.client('glue')

def lambda_handler(event, context):

    def GetTableScheme(database, table_name):
        table_info = client.get_table(DatabaseName=database, Name=table_name)['Table']
        table_scheme = table_info['StorageDescriptor']['Columns'] + table_info['PartitionKeys']
        # [{'Name': 'province', 'Type': 'string'}, {'Name': 'city', 'Type': 'string'}]
        return table_scheme

    def GetCreateTableSql(clickhouse_table, table_scheme):
        scheme_cols = reduce(lambda x,y: x+y, [f"`{i['Name']}` {i['Type'].capitalize()}," for i in table_scheme])
        scheme_cols = re.sub(",$", "", scheme_cols)
        sql_content = f"CREATE TABLE IF NOT EXISTS {clickhouse_table['table']}({scheme_cols}) ENGINE = MergeTree ORDER BY {clickhouse_table['orderby']} PARTITION BY {clickhouse_table['partitionby']} SETTINGS index_granularity = 8192;"
        return sql_content

    parameters = event['parameters']
    g_data_wide_table = parameters['g_data_wide_table']
    g_database_temp = parameters['g_database_temp']
    clickhouse_table_info = parameters['clickhouse_table_info']


    table_scheme = GetTableScheme(g_database_temp, g_data_wide_table)
    sql_content = GetCreateTableSql(clickhouse_table_info, table_scheme)
    print(sql_content)

    # "ec2-user@ec2-69-230-210-235.cn-northwest-1.compute.amazonaws.com.cn"
    # 在lmd内 '192.168.0.66'
    clickhouse_driver_client = Client(host='192.168.0.66')
    clickhouse_driver_client.execute(sql_content)
    run_id = event['parameter']['run_id']
    return {
        "run_id" : run_id
    }