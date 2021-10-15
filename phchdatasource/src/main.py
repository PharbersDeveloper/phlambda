import json
import urllib.request
from urllib.parse import urlencode

def lambda_handler(event, context):

    # 直接转proxy转发
    args = eval(event['body'])
    sql_query = { "query": args['query'] }

    res = urllib.request.urlopen(urllib.request.Request(
        url='http://192.168.0.66:9090/?' + urlencode(sql_query),
        method='GET'), timeout=5)

    rows = filter(lambda x: x != '', res.read().decode().split('\n'))

    # 这里没有任何的错误处理
    columns = args['schema']

    final_res = []
    for row in rows:
        cells = row.split("\t")

        tmp = {}
        for cell in cells:
            index = cells.index(cell)
            tmp[columns[index]] = cell

        final_res.append(tmp)

    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin':'*'},
        'body': json.dumps(final_res, ensure_ascii=False)
    }
