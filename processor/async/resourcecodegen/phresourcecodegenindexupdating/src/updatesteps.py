import json
from util.AWS.DynamoDB import DynamoDB


def update_steps(conf):
    db = DynamoDB()

    partition_key = f"""{conf["projectId"]}_{conf["jobFullName"]}"""

    # 根据key查询出原有的step，无就是空数组
    result = db.queryTableWithPartitionKey("step", "pjName", partition_key)["Items"]

    # 根据返回删除数据

    if len(result) > 0:
        keys = list(map(lambda item: {
            "DeleteRequest": {
                "Key": {
                    "pjName": partition_key,
                    "stepId": item["stepId"]
                }
            }
        }, result))
        db.batch_write("step", keys)

    # 将新的数据插入step
    steps = list(map(lambda item: {"PutRequest": {
        "Item": {
            "pjName": partition_key,
            "stepId": item["stepId"],
            "ctype": item["ctype"],
            "expressions": json.dumps(item["expressions"], ensure_ascii=False),
            "expressionsValue": item["expressionsValue"],
            "groupIndex": item.get("groupIndex", 0),
            "groupName": item.get("groupName", ""),
            "id": item["id"],
            "index": item["index"],
            "runtime": item["runtime"],
            "stepName": item["stepName"]
        }
    }}, conf["steps"]))

    db.batch_write("step", steps)

    # 将老数据返回给Old Image，没有就是空数组
    return result
