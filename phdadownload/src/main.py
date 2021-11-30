import json
from Common.ExportData.ChoiceMain import ChoiceMain


def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": ChoiceMain().choice(event)
    }
