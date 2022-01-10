
from __future__ import print_function
from delegate.version import AppLambdaDelegate
import json


def lambda_handler(event, context):
    try:
        app = AppLambdaDelegate(event=event, context=context)

    except Exception as e:
        return {
            "statusCode": 503,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": str(e)})
        }
    else:
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"message": app.run()})
        }
