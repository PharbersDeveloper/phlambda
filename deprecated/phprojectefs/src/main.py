import os, sys
import logging
import json

from createEfs import CreateEfs
from deleteEfs import DeleteEfs


def execute(project_name, operate_type):

    operate = {
        "create": CreateEfs(project_name=project_name, operate_type=operate_type),
        "delete": DeleteEfs(project_name=project_name, operate_type=operate_type)
    }

    operate.get(operate_type).execute()


def lambda_handler(event, context):
    '''
    event content:
        {
            "project_name": "autorawdata",
            "operator_type": "create"
        }
    '''

    if 'Records' in event:
        records = event['Records'][0]
        if 'EventSource' in records and records['EventSource'] == 'aws:sns':
            message = records['Sns']['Message']
            event = json.loads(message)

    project_name = event.get("project_name")
    operate_type = event.get("operator_type")

    execute(project_name, operate_type)
