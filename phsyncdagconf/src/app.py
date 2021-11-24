from __future__ import print_function
from delegate.SyncDagConfToDynamoDB import SyncDagConfToDynamoDB


def lambda_handler(event, context):
    print(event)
    app = SyncDagConfToDynamoDB(event=event, context=context)
    app.exec()
