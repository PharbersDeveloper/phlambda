import os
import constants.DefinValue as DV
from util.ClieckHouse import ClickHouse
from util.AWS.DynamoDB import DynamoDB
from util.PhRedis import PhRedis
from boto3.dynamodb.conditions import Attr
from phprojectargs.projectArgs import ProjectArgs


def __create_dynamodb():
    return DynamoDB()
    # import base64
    # from util.AWS.STS import STS
    # sts = STS().assume_role(
    #     base64.b64decode(DV.ASSUME_ROLE_ARN).decode(),
    #     "Ph-Back-RW"
    # )
    # return DynamoDB(sts=sts)


def __create_clickhouse(projectId):
    args = ProjectArgs(projectId)
    proxies = args.get_proxy_list()
    # dynamodb = EXTERNAL_SERVICES["dynamodb"]
    # result = dynamodb.scanTable({
    #     "table_name": "resource",
    #     "limit": 100000,
    #     "expression": Attr("projectId").eq(projectId),
    #     "start_key": ""
    # })["data"]
    ip = os.environ[DV.CLICKHOUSE_HOST]
    if len(proxies) > 0:
        ip = proxies[0]
    return ClickHouse(host=ip, port=os.environ[DV.CLICKHOUSE_PORT])


def __create_redis():
    return PhRedis(host=os.environ[DV.REDIS_HOST], port=os.environ[DV.REDIS_PORT])


EXTERNAL_SERVICES = {
    "dynamodb": __create_dynamodb(),
    "clickhouse": __create_clickhouse,
    "redis": __create_redis(),
}

