import os
from utils.addversionrecord import AddVersionRecord


# 运行指定dag
def lambda_handler(event, context):
    AddVersionRecord(os.getenv("DATABASE")).insert_item_into_dynamodb_table()