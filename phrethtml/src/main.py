
import boto3
import json


def down_html(html_name):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket='general.pharbers.com', Key=f'html/{html_name.split("/")[-1]}')["Body"].read()
    return response


def lambda_handler(event, context):
    # 直接转proxy转发
    args = eval(event["body"])
    try:
        html_name = args.get("uuid")
        return {
            'statusCode': 200,
            'body': down_html(html_name)
        }
    except Exception as e:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": str(e)})
        }

