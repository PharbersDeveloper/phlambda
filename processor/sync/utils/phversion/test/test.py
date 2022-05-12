import boto3


dynamodb = boto3.resource("dynamodb", region_name="cn-northwest-1")

table = dynamodb.Table('version')

print(table.creation_date_time)
