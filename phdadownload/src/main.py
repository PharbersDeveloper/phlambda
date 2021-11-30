# import json
# from Common.ExportData.ChoiceMain import ChoiceMain
#
#
# def lambda_handler(event, context):
#
#     return {
#         "statusCode": 200,
#         "headers": {"Access-Control-Allow-Origin": "*"},
#         "body": ChoiceMain().choice(event)
#     }
# ssm get url


import json
import boto3

ssm_client = boto3.client('ssm', region='cn-northwest-1')
response = ssm_client.get_parameter(
    Name='projects_driver_args',
    WithDecryption=True|False
)
ssm_dict = json.loads(response.get('Parameter').get('Value'))
print(ssm_dict)
