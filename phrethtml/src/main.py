import boto3


def down_html(html_name):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket='general.pharbers.com', Key=f'html/{html_name}.html')["Body"].read()
    return response


def lambda_handler(event, context):
    # 直接转proxy转发
    args = eval(event["body"])
    html_name = args.get("uuid")
    return down_html(html_name)
