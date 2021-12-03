import json
from Common.ExportData.ChoiceMain import ChoiceMain


def lambda_handler(event, context):

    try:
        result = ChoiceMain().choice(event)

    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e)}, ensure_ascii=False)
        }
    else:
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": result}, ensure_ascii=False)
        }
