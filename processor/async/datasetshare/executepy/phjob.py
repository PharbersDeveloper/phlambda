# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""

import boto3
import json
from functools import reduce
from boto3.dynamodb.conditions import Key
from pyspark.sql.functions import lit, col, struct, to_json, json_tuple
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL

logger = phs3logger("share emr log", LOG_DEBUG_LEVEL)

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


def write_to_path(share_num, mode, df, col_of_partitionBy, path_of_write):
    try:
        df.repartition(share_num).write.format("parquet").mode(mode).partitionBy \
            (col_of_partitionBy).parquet(path_of_write)
        write_info = f"{path_of_write} 写入成功"
    except Exception as e:
        print(e)
        write_info = f"{path_of_write} 写入失败"
    print(write_info)
    return write_info

def get_ds_with_index(dsName, projectId):

    dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")
    ds_table = dynamodb_resource.Table('dataset')
    res = ds_table.query(
        IndexName='dataset-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").begins_with(dsName)
    )
    return res["Items"][0]


def execute(**kwargs):
    spark = kwargs["spark"]
    ph_share = json.loads(kwargs.get("ph_conf", {}))
    shares = ph_share.get("shares")
    tenantId = ph_share.get("tenantId")
    company = ph_share.get("company")
    sourceProjectId = ph_share.get("projectId")

    lake_path = "s3://ph-platform/2020-11-11/lake"

    for shareItem in shares:
        sourcePath = f"{lake_path}/{company}/{sourceProjectId}/{shareItem['source']}"
        #---- get df ------#
        df = spark.read.parquet(sourcePath)
        logger.info(shareItem["sourceSelectVersions"])
        df = df.where(df["traceId"].isin(shareItem["sourceSelectVersions"]))
        df = convert_normal_df(df, convert_union_schema(df)).drop("traceId")

        #---- target Path -----------#
        if shareItem["targetCat"] == "catalog":
            targetPath = f"{lake_path}/{company}/{tenantId}/{shareItem['target']}"
            partitionByCols = [x["name"] for x in shareItem['targetPartitionKeys']]

            #---- get schema of target table --------------------#
            targetDsItem = get_ds_with_index(dsName=shareItem["target"], projectId=sourceProjectId)
            targetSchema = json.loads(targetDsItem["schema"]) if isinstance(targetDsItem["schema"], str) else targetDsItem["schema"]

            if len(targetSchema) == 0:
                write_to_path(share_num=1, mode="overwrite", df=df, col_of_partitionBy=partitionByCols, path_of_write=targetPath)
            else:
                write_to_path(share_num=1, mode="append", df=df, col_of_partitionBy=partitionByCols, path_of_write=targetPath)

        # TODO intermediate ,uploaded 如果需要后续添加处理逻辑

    return {'out_df': {}}
