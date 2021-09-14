
import json
import boto3

def lambda_handler(event, context):

    print(event)

    p_output = event['parameters'][0]['p_output']
    glue_client = boto3.client('glue')
    response = glue_client.get_crawlers()
    for crawler in response['Crawlers']:
        if crawler['Targets']['S3Targets'][0]['Path'] in p_output:
            database = crawler['DatabaseName']


    table_name = p_output.split("/")[-1]
    Message = {
        "name": table_name,
        "Subject": "glueindex",
        "database": database
    }
    Message_str = json.dumps(Message, ensure_ascii=False)
    MessageAttributes= {
        "action": {
            "DataType": "String",
            "StringValue": "update"
        },
        "type": {
            "DataType": "String",
            "StringValue": "table"
        }
    }

    glueindex = {
        "Records": [
            {
                "Sns": {
                    "Subject": "glueindex",
                    "Message": Message_str,
                    "MessageAttributes": MessageAttributes
                }
            }
        ]
    }


    lmd_client = boto3.client("lambda")
    response = lmd_client.invoke(
        FunctionName='phglueindex',
        Payload=json.dumps(glueindex).encode()
    )
