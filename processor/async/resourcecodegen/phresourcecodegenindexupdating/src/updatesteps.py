import decimal
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from util.AWS.DynamoDB import DynamoDB

dynamodb = boto3.client("dynamodb")


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        super(DecimalEncoder, self).default(o)


def query_step(partition_key):
    print(partition_key)
    response = dynamodb.query(
        TableName="step",
        KeyConditionExpression='#pjName = :pjName',
        ExpressionAttributeNames={
            '#pjName': 'pjName',
        },
        ExpressionAttributeValues={
            ':pjName': {
                'S': partition_key
            }}
    )
    result = {}
    print(response.get("Items"))
    item = response.get("Items")[0] if len(response.get("Items")) else {}
    if item:
        for key, value in item.items():
            result[key] = list(value.values())[0]
    return [result] if result else []


def update_steps(conf):
    partition_key = f"""{conf["projectId"]}_{conf["jobFullName"]}"""

    # 根据key查询出原有的step，无就是空数组
    result = query_step(partition_key)

    # 根据返回删除数据

    if len(result) > 0:
        keys = list(map(lambda item: {
                "pjName": {'S': partition_key},
                "stepId": {'S': item["stepId"]}
        }, result))
        for key in keys:
            dynamodb.delete_item(
                TableName="step",
                Key=key
            )

    # 将新的数据插入step

    steps = list(map(lambda item: {
        "item": {
            "pjName": {"S": partition_key},
            "stepId": {"S": item["stepId"]},
            "ctype": {"S": item["ctype"]},
            "expressions": {"S": json.dumps(item["expressions"], ensure_ascii=False)},
            "expressionsValue": {"S": item["expressionsValue"]},
            "groupIndex": {"S": str(item.get("groupIndex", 0))},
            "groupName": {"S": item.get("groupName", "")},
            "id": {"S": item["id"]},
            "index": {"S": str(item["index"])},
            "runtime": {"S": item["runtime"]},
            "stepName": {"S": item["stepName"]}
        },
        "table_name": "step"
    }, conf["steps"]))

    for step in steps:
        print(step["item"])
        response = dynamodb.put_item(
            TableName="step",
            Item=step["item"]
        )

    # 将老数据返回给Old Image，没有就是空数组
    return json.loads(json.dumps(result, cls=DecimalEncoder, ensure_ascii=False))


