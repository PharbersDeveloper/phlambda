
import os
import boto3
import time
import json
import urllib.request
from redis import Redis, ConnectionPool
from urllib.parse import urlencode
app_name = os.environ.get('APP_NAME')
redis = {
    'host': os.environ.get('HOST'),
    'port': os.environ.get('PORT')
}
pool = ConnectionPool(**redis, max_connections=10, decode_responses=True)
rediscli:Redis = Redis(connection_pool=pool)

# ssm get url
client = boto3.client('ssm')
response = client.get_parameter(
    Name='projects_args',
    WithDecryption=True|False
)
ssm_dict = json.loads(response.get('Parameter').get('Value'))
default_list = ssm_dict.keys()


def lambda_handler(event, context):
    args = eval(event['body'])
    default = args.get('default', 'default')
    is_default = default if default in default_list else None

    if is_default and rediscli.setnx(f'{app_name}', time.time()):
        rediscli.expire(f'{app_name}', 60)
        url = ssm_dict.get(is_default)
        # 直接转proxy转发
        args = eval(event['body'])
        print(args)
        sql_query = args['query']
        print(sql_query)
        query = sql_query.encode()

        res = urllib.request.urlopen(urllib.request.Request(
            url=url, data=query,
            method='POST'), timeout=5)

        print(res)
        rediscli.delete(f"{app_name}")

        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin':'*'},
            'body': 'success'
        }
