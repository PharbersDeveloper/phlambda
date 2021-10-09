import json
import urllib.request
from urllib.parse import urlencode

def lambda_handler(event, context):
    # 直接转proxy转发
    args = eval(event['body'])
    print(args)
    sql_query = args['query']
    print(sql_query)
    query = sql_query.encode()

    res = urllib.request.urlopen(urllib.request.Request(
        url='http://192.168.0.66:9090/?', data=query,
        method='POST'), timeout=5)

    print(res)

    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin':'*'},
        'body': 'success'
    }