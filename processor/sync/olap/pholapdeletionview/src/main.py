import json
import boto3
import http.client


def execute_sql(sql, tenant_id):
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(
        Name=tenant_id,
    )
    value = json.loads(response["Parameter"]["Value"])
    conn = http.client.HTTPConnection(host=value["olap"]["PrivateIp"], port="8123")
    # conn = http.client.HTTPConnection(host="127.0.0.1", port="18123")
    headers = {
        'Content-Type': 'text/plain'
    }
    conn.request("POST", "/", sql.encode("utf-8"), headers)
    # response = conn.getresponse()
    # data = response.read().decode("utf-8")
    # return json.loads(data) if len(data) > 0 else {"data": "None"}


def lambda_handler(event, context):
    event = json.loads(event["body"])
    view_name = f"{event['project_id']}_{event['job_name']}"
    execute_sql(f"DROP VIEW `{view_name}`", event["tenant_id"])
    result = {
        "status": "success"
    }
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(result, ensure_ascii=False)
    }
