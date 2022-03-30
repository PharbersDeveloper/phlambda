# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""

import boto3
import re
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL
from clickhouse_driver import Client


def execute(**kwargs):

    def deleteTableSql(table, database='default'):
        sql_content = f"DROP TABLE {database}.`{table}`"
        return sql_content

    def get_project_ip(project_id, project_name, logger):

        def name_convert_to_camel(name):
            return re.sub(r'(_[a-z])', lambda x: x.group(1)[1], name.lower())

        target_name = name_convert_to_camel(project_name)
        dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")
        table = dynamodb_resource.Table("resource")
        key = {
            "projectName": target_name,
            "projectId": project_id
        }
        res = table.get_item(
            Key=key,
        )
        resource_item = res.get("Item")
        project_ip = resource_item.get("projectIp")

        return project_ip


    def clickhouse_client(project_id, project_name, logger):
        project_ip = get_project_ip(project_id, project_name, logger)
        ch_client = Client(
            host=project_ip
        )

        return ch_client

    spark = kwargs["spark"]()
    ph_conf = kwargs.get("ph_conf")
    projectId = ph_conf.get("projectId")
    projectName = ph_conf.get("projectName")
    datasetName = ph_conf.get("datasetName")
    version = ph_conf.get("datasetVersion")
    sample = ph_conf.get("sample")
    company = ph_conf.get("company")
    # 从s3 读取数据
    path = f"s3://ph-platform/2020-11-11/lake/{company}/{projectId}/{datasetName}/"
    df = spark.read.parquet(path)
    df = df.where(df["version"].isin(version))

    # 按照 sample 对数据进行处理
    df_sample = sample.split("_")[0]
    df_count = sample.split("_")[1]
    if df_sample == "F":
        sample_df = df.limit(int(df_count) * 10000)
    elif df_sample == "R":
        fraction = float(int(df_count) * 20000 / df.count())
        if fraction >= 1.0:
            fraction = 1.0
        sample_df = df.sample(withReplacement=False, fraction=fraction)
        sample_df = sample_df.limit(int(df_count) * 10000)

    # 获取projectip
    projectIp = get_project_ip(projectId, projectName)
    # 创建clickhouse client
    ch_client = clickhouse_client(projectId, projectName)
    # 删除已有的表
    table_name = projectId + "_" + datasetName
    delete_sql = deleteTableSql(table_name)
    ch_client.execute(delete_sql)
    # 写入clickhouse
    sample_df.write.format("jdbc").mode("append") \
        .option("url", f"jdbc:clickhouse://{projectIp}:8123/default") \
        .option("dbtable", f"`{table_name}`") \
        .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
        .option("user", "default") \
        .option("password", "") \
        .option("batchsize", 1000) \
        .option("socket_timeout", 300000) \
        .option("numPartitions", 2) \
        .option("rewrtieBatchedStatements", True) \
        .save()

    return {'out_df': {}}

