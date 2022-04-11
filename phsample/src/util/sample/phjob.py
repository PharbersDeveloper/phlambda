# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""

import boto3
import json
import time
import re
from pyspark.sql.functions import lit
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL
from clickhouse_driver import Client


def execute(**kwargs):
    logger = phs3logger(kwargs["job_id"], LOG_DEBUG_LEVEL)
    dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")
    def deleteTableSql(table, database='default'):
        sql_content = f"DROP TABLE IF EXISTS {database}.`{table}`"
        return sql_content

    def addVersion(df, version, version_colname='version'):
        df = df.withColumn(version_colname, lit(version))
        return df

    def get_project_ip(project_id, project_name):

        def name_convert_to_camel(name):
            return re.sub(r'(_[a-z])', lambda x: x.group(1)[1], name.lower())

        target_name = name_convert_to_camel(project_name)

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

    def clickhouse_client(project_id, project_name):
        project_ip = get_project_ip(project_id, project_name)
        ch_client = Client(
            host=project_ip
        )

        return ch_client

    def createClickhouseTableSql(df, table_name, database='default', order_by='', partition_by='version'):
        def getSchemeSql(df):
            file_scheme = df.dtypes
            sql_scheme = ""
            for i in file_scheme:
                if i[0] in [order_by, partition_by]:
                    # 主键和分区键不支持null
                    coltype = i[1].capitalize()
                else:
                    coltype = f"Nullable({i[1].capitalize()})"
                sql_scheme += f"`{i[0]}` {coltype},"
            sql_scheme = re.sub(r",$", "", sql_scheme)
            return sql_scheme
        return f"CREATE TABLE IF NOT EXISTS {database}.`{table_name}`({getSchemeSql(df)}) ENGINE = MergeTree() ORDER BY tuple({order_by}) PARTITION BY {partition_by};"

    def get_dynamodb_item(table_name, key):
        table = dynamodb_resource.Table(table_name)
        res = table.get_item(
            Key=key,
        )
        return res.get("Item")

    def put_dynamodb_item(table_name, item):
        table = dynamodb_resource.Table(table_name)
        table.put_item(
            Item=item
        )

    def put_scheme_to_dataset(output_id, project_id, schema_list, output_version):

        table_name = "dataset"
        key = {
            "id": output_id,
            "projectId": project_id
        }
        dataset_item = get_dynamodb_item(table_name, key)
        dataset_item.update({"schema": json.dumps(schema_list, ensure_ascii=False)})
        dataset_item.update({"version": json.dumps(output_version, ensure_ascii=False)})
        put_dynamodb_item(table_name, dataset_item)

    def putOutputSchema(output_id, project_id, df, output_version):

        def getSchemaSql(df):
            schema_list = []
            file_scheme = df.dtypes
            for i in file_scheme:
                schema_map = {}
                schema_map["src"] = i[0]
                schema_map["des"] = i[0]
                schema_map["type"] = i[1].capitalize().replace('Int', 'Double')
                schema_list.append(schema_map)
            return schema_list

        schema_list = getSchemaSql(df)
        res = put_scheme_to_dataset(output_id, project_id, schema_list, output_version)

    spark = kwargs["spark"]()
    ph_conf = json.loads(kwargs.get("ph_conf", {}))
    sourceProjectId = ph_conf.get("sourceProjectId")
    targetProjectId = ph_conf.get("targetProjectId")
    projectName = ph_conf.get("projectName")
    datasetName = ph_conf.get("datasetName")
    datasetId = ph_conf.get("datasetId")
    sample = ph_conf.get("sample")
    owner = ph_conf.get("showName")
    company = ph_conf.get("company")
    version = owner + "_" + datasetName + "_" + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    # 从s3 读取数据
    path = f"s3://ph-platform/2020-11-11/lake/{company}/{sourceProjectId}/{datasetName}/"
    df = spark.read.parquet(path)

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

    logger.debug("sample_df 创建完成")
    # 获取projectip
    projectIp = get_project_ip(targetProjectId, projectName)
    logger.debug("ip 获取完成")
    logger.debug(projectIp)
    # 创建clickhouse client
    ch_client = clickhouse_client(targetProjectId, projectName)
    # 如果表已经存在 删除已有的表
    table_name = targetProjectId + "_" + datasetName
    delete_sql = deleteTableSql(table_name)
    ch_client.execute(delete_sql)

    # 创建创表语句
    sql_create_table = createClickhouseTableSql(sample_df, table_name)
    logger.debug(sql_create_table)
    ch_client.execute(sql_create_table)


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
        .option("rewriteBatchedStatements", True) \
        .save()

    putOutputSchema(datasetId, targetProjectId, sample_df, version)

    return {'out_df': {}}

