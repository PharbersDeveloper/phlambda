import boto3
import json


s3 = boto3.client('s3')

# 输入参数 {    "runId": "",    "dagName": "" }
#
# 参数存放在s3中需要 读取json并返回给前端
#
# Bucket:  ph-platform
#
# Key: 
#
# '2020-11-11/jobs/statemachine/pharbers/' + dagName + '/' + event['runnerId'] + '/' + 'conf_user.json'


def get_data(dagName, runnerId):
    key = f'2020-11-11/jobs/statemachine/pharbers/{dagName}/{runnerId}/conf_user.json'
    response = s3.get_object(Bucket="ph-platform", Key=key)
    return json.loads(response.get('Body').read())


def lambda_handler(event, context):
    try:
        data = get_data(**eval(event["body"]))
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": data, "status": 0}, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e), "status": 1}, ensure_ascii=False)
        }
