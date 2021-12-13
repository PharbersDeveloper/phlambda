import constants.DefinValue as DV
from util.ClieckHouse import ClickHouse
from util.AWS.DynamoDB import DynamoDB


def __create_dynamodb():
    import base64
    from util.AWS.STS import STS
    sts = STS().assume_role(
        base64.b64decode(DV.ASSUME_ROLE_ARN).decode(),
        "Ph-Back-RW"
    )
    return DynamoDB(sts=sts)


def __create_clickhouse():
    return ClickHouse(host="192.168.16.117", port="9000")


EXTERNAL_SERVICES = {
    "dynamodb": __create_dynamodb(),
    "clickhouse": __create_clickhouse()
}

