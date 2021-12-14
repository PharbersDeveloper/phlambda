from __future__ import print_function
from delegate.version import AppLambdaDelegate


def lambda_handler(event, context):
    app = AppLambdaDelegate(event=event, context=context)
    return app.run()
