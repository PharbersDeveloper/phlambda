import os
import constants.DefinValue as DV
from util.ClieckHouse import ClickHouse
from util.AWS.DynamoDB import DynamoDB
from util.PhRedis import PhRedis


def __create_dynamodb():
    return DynamoDB()
    # import base64
    # from util.AWS.STS import STS
    # sts = STS().assume_role(
    #     base64.b64decode(DV.ASSUME_ROLE_ARN).decode(),
    #     "Ph-Back-RW"
    # )
    # return DynamoDB(sts=sts)


def __create_clickhouse():
    return ClickHouse(host=os.environ[DV.CLICKHOUSE_HOST], port=os.environ[DV.CLICKHOUSE_PORT])


def __create_redis():
    return PhRedis(host=os.environ[DV.REDIS_HOST], port=os.environ[DV.REDIS_PORT])


EXTERNAL_SERVICES = {
    "dynamodb": __create_dynamodb(),
    "clickhouse": __create_clickhouse(),
    "redis": __create_redis(),
}

