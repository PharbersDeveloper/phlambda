from __future__ import print_function
from delegate.AppLambdaDelegate import AppLambdaDelegate


def lambda_handler(event, context):
    print(event)
    app = AppLambdaDelegate(event=event, context=context)
    app.exec()
