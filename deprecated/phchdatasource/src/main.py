import os
import json
import time

import boto3
import urllib.request
import logging
from urllib.parse import urlencode
from redis import Redis, ConnectionPool
from returen_data_type import adapter_list_of_dict, adapter_list_of_list

# app_name = 'phchdatasource'
app_name = os.environ.get('APP_NAME')
redis = {
    'host': os.environ.get('HOST'),
    'port': os.environ.get('PORT')
}

logger = logging.getLogger(f'{app_name}')

# ssm get url
client = boto3.client('ssm')
response = client.get_parameter(
    Name='projects_args',
    WithDecryption=True|False
)
ssm_dict = json.loads(response.get('Parameter').get('Value'))

# redis cli
pool = ConnectionPool(**redis, max_connections=10, decode_responses=True)
rediscli:Redis = Redis(connection_pool=pool)

commends = {
    'adapter_dict': adapter_list_of_dict,
    'adapter_list': adapter_list_of_list
}
default_list = ssm_dict.keys()


def lambda_handler(event, context):
    args = eval(event['body'])
    default = args.get('default', 'default')
    is_default = default if default in default_list else None

    if is_default and rediscli.setnx(f'{app_name}', time.time()):
        rediscli.expire(f'{app_name}', 60)
        url = ssm_dict.get(is_default)

        # 直接转proxy转发
        sql_query = { "query": args['query'] }

        res = urllib.request.urlopen(urllib.request.Request(
            url=url + urlencode(sql_query),
            method='GET'), timeout=5)

        rows = filter(lambda x: x != '', res.read().decode().split('\n'))

        # 这里没有任何的错误处理
        logger.info(args)
        columns = args['schema']
        commend = args.get('adapter')

        if commend in commends.keys():
            final_res = commends[commend](rows=rows, columns=columns)

        else:
            final_res = f"adapter {event.get('adapter')} error"
            logger.error(f"get adapter error: {event.get('adapter')}")

    else:
        final_res = 'error'
        logger.error(f"get url error !!!")

    rediscli.delete(f"{app_name}")

    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(final_res, ensure_ascii=False)
    }
