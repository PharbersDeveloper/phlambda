import json

# TODO 差获取ClickHouse数据通过Panda是写入临时目录 （Lambda）
# TODO 通过写入临时目录的文件上传到S3的指定目录下
# TODO 根据S3指定的目录文件生成signed-url返回给前端


def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps("", ensure_ascii=False)
    }
