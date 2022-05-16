# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""

import boto3
import json
import time

import re
from functools import reduce
from pyspark.sql.functions import lit, col, struct, to_json, json_tuple
from pyspark.sql.types import StructType, StringType
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL
from clickhouse_driver import Client
from boto3.dynamodb.conditions import Key


def execute(**kwargs):
    logger = phs3logger(kwargs["job_id"], LOG_DEBUG_LEVEL)
    dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")

    # 对多TraceId取Schema的col的并集（暂时先不管类型）
    def convert_union_schema(df):
        rows = df.select("traceId", "schema").distinct().collect()
        return list(reduce(lambda pre, next: set(pre).union(set(next)), list(map(lambda row: [schema["name"] for schema in json.loads(row["schema"])], rows))))

    # 将统一Schema的DF转成正常的DataFrame
    def convert_normal_df(df, cols):
        return df.select(col("traceId"),json_tuple(col("data"), *cols)) \
            .toDF("traceId", *cols)

    def get_ds_with_index(dsName, projectId):

        ds_table = dynamodb_resource.Table('dataset')
        res = ds_table.query(
            IndexName='dataset-projectId-name-index',
            KeyConditionExpression=Key("projectId").eq(projectId)
                                   & Key("name").begins_with(dsName)
        )
        return res["Items"][0]

    def uploaded_s3_df(lake_prefix, name, project_id):

        schemas = json.loads(get_ds_with_index(name, project_id).get("schema"))
        schema_type = StructType()

        for item in schemas:
            schema_type = schema_type.add(item["src"], StringType())

        reader = spark.read.schema(schema_type)

        df = reader.csv(f"{lake_prefix}{project_id}/{name}")
        logger.debug("从s3读取df")
        logger.debug(df.count())
        logger.debug("从s3读取df")
        # if len(version) != 0:
        #     df = df.where(df["version"].isin(version))
        # logger.debug(df.count())
        return df

    def deleteTableSql(table, database='default'):
        sql_content = f"DROP TABLE IF EXISTS {database}.`{table}`"
        return sql_content

    def get_project_ip(project_id, project_name):

        ssm_client = boto3.client('ssm', region_name="cn-northwest-1")
        response = ssm_client.get_parameter(
            Name=project_id,
        )
        value = json.loads(response["Parameter"]["Value"])
        project_ip = value.get("proxies")[0]

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


    def put_dynamodb_item(table_name, item):
        table = dynamodb_resource.Table(table_name)
        table.put_item(
            Item=item
        )

    def put_scheme_to_dataset(output_name, project_id, schema_list, output_version):

        table_name = "dataset"
        dataset_item = get_ds_with_index(output_name, project_id)
        dataset_item.update({"schema": json.dumps(schema_list, ensure_ascii=False)})
        dataset_item.update({"version": json.dumps(output_version, ensure_ascii=False)})
        put_dynamodb_item(table_name, dataset_item)

    def putOutputSchema(output_name, project_id, df, output_version):

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
        res = put_scheme_to_dataset(output_name, project_id, schema_list, output_version)


    spark = kwargs["spark"]()
    ph_conf = json.loads(kwargs.get("ph_conf", {}))
    sourceProjectId = ph_conf.get("sourceProjectId")
    targetProjectId = ph_conf.get("targetProjectId")
    projectName = ph_conf.get("projectName")
    datasetName = ph_conf.get("datasetName")
    datasetId = ph_conf.get("datasetId")
    datasetType = ph_conf.get("datasetType")
    sample = ph_conf.get("sample")
    owner = ph_conf.get("showName")
    company = ph_conf.get("company")
    version = owner + "_" + datasetName + "_" + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())

    path = f"s3://ph-platform/2020-11-11/lake/{company}/{sourceProjectId}/{datasetName}/"

    logger.debug("datasetType")
    # 从s3 读取数据
    # 1 uploaded
    if datasetType == "uploaded":
        logger.debug("uploaded sample")
        lake_prefix = f"s3://ph-platform/2020-11-11/lake/{company}/"
        logger.debug(lake_prefix)
        df = uploaded_s3_df(lake_prefix, datasetName, sourceProjectId)
        logger.debug(df.count())
    # 2 intermediate
    if datasetType == "intermediate":
        logger.debug("intermediate sample")
        df = spark.read.parquet(path)
        df = convert_normal_df(df, convert_union_schema(df))
        logger.debug(df.count())
    # 3 catalog
    if datasetType == "catalog":
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
    logger.debug(sample_df.count())
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

    logger.debug(sample_df.count())
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

    putOutputSchema(datasetName, targetProjectId, sample_df, version)

    return {'out_df': {}}

