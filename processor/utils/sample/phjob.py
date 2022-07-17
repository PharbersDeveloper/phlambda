# -*- coding: utf-8 -*-

import json
import boto3

from pyspark.sql.types import StructType, StringType, DoubleType, LongType
from pyspark.sql.functions import lit, col, struct, to_json, json_tuple, when, split
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL
from functools import reduce
from clickhouse_driver import Client
from boto3.dynamodb.conditions import Key

dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")


# 解决在读取中间型DF Schema Type冲突后的选择
# 在同Schema Col类型冲突后优先选择非String类型的描述 list(filter(lambda item: item["type"] != "String", values))
# 这部分在后续扩展时不是很友好，原因是后续会扩展很多类型
def conflict_schema_type_resolve(df):
    from itertools import groupby
    rows = df.select("traceId", "schema").distinct().withColumn("__run_id", split("traceId", "\+00:00")[0]).orderBy(
        "__run_id", ascending=True).collect()
    schema_strs = list(reduce(lambda schema_pre, schema_next: set(schema_pre).union(set(schema_next)),
                              list(map(lambda row: [f"{schema['name']}:{schema['type']}" for schema in
                                                    json.loads(row["schema"])], rows))))
    group_schemas = groupby(
        list(map(lambda item: {"src": item.split(":")[0], "type": item.split(":")[1].capitalize()}, schema_strs)),
        key=lambda x: x["src"])
    schemas = []
    for key, group in group_schemas:
        values = list(group)
        if len(values) > 1:
            values = list(filter(lambda item: item["type"] != "String", values))
        schemas += values
    return schemas


# 根据Schema类型转换DF类型
def transform_schema_type(df, schemas):
    pattern = "^-?[0-9]*.?[0-9]*$rep"

    choose_schema_type = {
        "string": StringType(),
        "double": DoubleType(),
        "long": LongType(),
        "bigint": LongType()
    }

    def transform_number(default="double"):
        transform_df = df.withColumn(f"""__{item["src"]}_type""",
                                     when(col(item["src"]).rlike(pattern), "true").when(col(item["src"]).isNull(),
                                                                                        "true").otherwise("false"))
        if transform_df.filter(f"""`__{item["src"]}_type` = 'false'""").count() == 0:
            transform_df = transform_df.withColumn(item["src"], col(item["src"]).cast(choose_schema_type[default]))
        else:
            transform_df = transform_df.withColumn(item["src"], col(item["src"]).cast(StringType()))
        return transform_df

    def transform_string(default="string"):
        return df.withColumn(item["src"], col(item["src"]).cast(choose_schema_type[default]))

    choose_schema_func = {
        "string": transform_string,
        "double": transform_number,
        "long": transform_number
    }

    types = list(set(map(lambda item: item["type"].lower(), schemas)))
    if len(types) == 1 and types[0] == "string":
        return df

    for item in schemas:
        df = choose_schema_func[item["type"].lower()](item["type"].lower()).drop(f"""__{item["src"]}_type""")
    return df


# 获取DataFrame Schema转JSON字符串
def get_df_schema2json(df):
    schema_list = list(filter(lambda item: item["name"] != "traceId",
                              list(map(lambda item: {"name": item["name"], "type": item["type"]},
                                       df.schema.jsonValue()["fields"]))))
    return json.dumps(schema_list, ensure_ascii=False)


# 将DataFrame统一Schema一致性
def convert_consistency_schema(df, schema):
    return df.withColumn("data",
                         to_json(struct(*[col(c) for c in list(map(lambda item: item["name"], json.loads(schema)))]))) \
        .withColumn("schema", lit(schema)).select("traceId", "schema", "data")


# 对多TraceId取Schema的col的并集
def convert_union_schema(df):
    rows = df.select("traceId", "schema").distinct().collect()
    return list(reduce(lambda schema_pre, schema_next: set(schema_pre).union(set(schema_next)),
                       list(map(lambda row: [schema["name"] for schema in json.loads(row["schema"])], rows))))


# 将统一Schema的DF转成正常的DataFrame
def convert_normal_df(df, cols):
    return df.select(col("traceId"), json_tuple(col("data"), *cols)).toDF("traceId", *cols)


# 根据DynamoDB index查询
def get_ds_with_index(ds_name, project_id):
    ds_table = dynamodb_resource.Table("dataset")
    return ds_table.query(
        IndexName="dataset-projectId-name-index",
        KeyConditionExpression=Key("projectId").eq(project_id) & Key("name").begins_with(ds_name)
    )["Items"][0]


# DynamoDB增加更新操作
def put_dynamodb_item(table_name, item):
    table = dynamodb_resource.Table(table_name)
    table.put_item(Item=item)


# 读取S3文件转为DF
def s3_to_df(spark, suffix, path, options=None):
    def reader_csv():
        if options:
            return spark.read.schema(options).csv(path)
        return spark.read.csv(path, header=True)

    def reader_parquet():
        return spark.read.parquet(path)

    reader_funcs = {
        "csv": reader_csv,
        "parquet": reader_parquet
    }
    df = reader_funcs[suffix]()
    # if len(versions) != 0:
    #     df = df.where(df["traceId"].isin(versions))
    return df


# 针对Uploaded的类型处理
def load_uploaded_s3_df(spark, path, schemas=None):
    suffix = "csv"
    schema_type = StructType()
    for item in schemas:
        schema_type = schema_type.add(item["src"], StringType())
    return transform_schema_type(s3_to_df(spark, suffix, path, schema_type), schemas)


# intermediate Parquet
def load_intermediate_df(spark, path, schemas=None):
    suffix = "parquet"
    df = s3_to_df(spark, suffix, path)
    parquet_df = convert_normal_df(df, convert_union_schema(df)).drop("traceId")
    return transform_schema_type(parquet_df, conflict_schema_type_resolve(df))


# Catalog Parquet
def load_catalog_df(spark, path, schemas=None):
    suffix = "parquet"
    return transform_schema_type(s3_to_df(spark, suffix, path), schemas)


read_data_cat = {
    "uploaded": load_uploaded_s3_df,
    "intermediate": load_intermediate_df,
    "catalog": load_catalog_df
}


# build Create Sql
def build_create_sql(df, table_name, database="default", order_by="", partition_by="version"):
    sql_cols = list(map(lambda item: f"`{item[0]}` {item[1].capitalize()}" if item[0] in [order_by, partition_by]
    else f"`{item[0]}` Nullable({item[1].capitalize()})", df.dtypes))
    sql_schema = ",".join(sql_cols)
    return f"CREATE TABLE IF NOT EXISTS {database}.`{table_name}`({sql_schema}) ENGINE = MergeTree() ORDER BY tuple({order_by}) PARTITION BY {partition_by};"


def execute(**kwargs):
    logger = phs3logger("sample_log", LOG_DEBUG_LEVEL)
    spark = kwargs["spark"]
    tenantIp = kwargs.get("tenant_ip")
    ph_conf = json.loads(kwargs.get("ph_conf", {}))
    sourceProjectId = ph_conf.get("sourceProjectId")
    targetProjectId = ph_conf.get("targetProjectId")
    datasetName = ph_conf.get("datasetName")
    datasetType = ph_conf.get("datasetType")
    sample = ph_conf.get("sample")
    tenant = ph_conf.get("company")
    lake_prefix = f"s3://ph-platform/2020-11-11/lake/{tenant}/"
    path = f"{lake_prefix}{sourceProjectId}/{datasetName}/"

    schemas = json.loads(get_ds_with_index(datasetName, sourceProjectId).get("schema"))

    df = read_data_cat[datasetType](spark, path, schemas)

    # 按照 sample 对数据进行处理
    df_sample = sample.split("_")[0]
    df_count = sample.split("_")[1]

    def sample_first():
        return df.limit(int(df_count) * 10000)

    def sample_random():
        fraction = float(int(df_count) * 20000 / df.count())
        if fraction >= 1.0:
            fraction = 1.0
        return df.sample(withReplacement=False, fraction=fraction).limit(int(df_count) * 10000)

    sample_strategy = {
        "F": sample_first,
        "R": sample_random
    }

    sample_df = sample_strategy[df_sample]().na.fill("None").drop("traceId")

    # 创建ClickHouse Client
    ch_client = Client(host=tenantIp)

    table_name = targetProjectId + "_" + datasetName
    ch_client.execute(f"DROP TABLE IF EXISTS default.`{table_name}`")

    create_sql = build_create_sql(sample_df, table_name)
    logger.debug(create_sql)
    ch_client.execute(create_sql)

    sample_df.show(100000, False)

    sample_df.write.format("jdbc").mode("append") \
        .option("url", f"jdbc:clickhouse://{tenantIp}:8123/default") \
        .option("dbtable", f"`{table_name}`") \
        .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
        .option("user", "default") \
        .option("password", "") \
        .option("batchsize", 1000) \
        .option("socket_timeout", 300000) \
        .option("numPartitions", 2) \
        .option("rewriteBatchedStatements", True) \
        .save()

    return {"out_df": {}}
