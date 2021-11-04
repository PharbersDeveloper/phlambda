from __future__ import print_function
from delegate.AppLambdaDelegate import AppLambdaDelegate


def lambda_handler(event, context):
    app = AppLambdaDelegate(event=event, context=context)
    return app.exec()
