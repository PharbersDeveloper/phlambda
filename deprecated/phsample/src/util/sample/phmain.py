# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""
import json
import click
import time
import traceback
import requests
import re
import boto3

from phjob import execute
from clickhouse_driver import Client
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL
from phcli.ph_max_auto.ph_hook.ph_hook import exec_before, exec_after
from pyspark.sql.functions import lit

dynamodb_resource = boto3.resource("dynamodb", region_name="cn-northwest-1")

def create_df(input_ds, spark, output_version, project_id, project_name, logger):

    def create_clickhouse_df(name, version):

        project_ip = get_project_ip(project_id, project_name, logger)
        df = spark.read.format("jdbc") \
            .option("url", f"jdbc:clickhouse://{project_ip}:8123") \
            .option("dbtable", "`" +project_id + "_" + name + "`") \
            .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
            .option("user", "default") \
            .option("password", "") \
            .option("fetchsize", "500000").load()
        df = df.where(df["version"].isin(version))
        return df

    def create_s3_df(path):

        if path.endswith(".csv"):
            df = spark.read.csv(path, header=True)
        else:
            df = spark.read.parquet(path)
        df = df.where(df["version"].isin(version))
        return df

    def create_catalog_df(database, tableName):
        df = spark.sql(f"select * from {database}.{tableName}")
        return df

    def lowerColumns(df):
        df = df.toDF(*[i.lower() for i in df.columns])
        return df

    version = input_ds.get("version")
    if len(version) == 0:
        version.append(output_version)
    name = input_ds.get("name")

    if input_ds.get("cat") == "uploaded":
        df = create_clickhouse_df(name, version)
    elif input_ds.get("cat") == "input_index":
        prop = input_ds.get("prop")
        path = prop.get("path")
        df = create_s3_df(path)
    elif input_ds.get("cat") == "catalog":
        prop = input_ds.get("prop")
        databaseName = prop.get("databaseName")
        tableName = prop.get("tableName")
        df = create_catalog_df(databaseName, tableName)
    else:
        path = f"s3://ph-platform/2020-11-11/lake/pharbers/{project_id}/{name}/"
        df = create_s3_df(path)

    df = lowerColumns(df)
    
    return df

def readClickhouse(inputs, kwargs, project_id, project_name, output_version, logger):
    df_map = {}
    spark = kwargs['spark']()
    ds_list = kwargs.get("ds_conf")
    name_ds_map_dict = {}
    for ds in ds_list:
        name_ds_map_dict.update({ds.get("name"): ds})
    logger.debug("name_ds_map_dict")
    logger.debug(name_ds_map_dict)
    for input_ds_name in inputs:
        if input_ds_name in name_ds_map_dict.keys():
            input_df = create_df(name_ds_map_dict.get(input_ds_name), spark, output_version, project_id, project_name, logger)
            df_map.update({"df_" +input_ds_name: input_df})
        else:
            input_ds = {
                "name": input_ds_name,
                "version": output_version.split(","),
                "cat": "intermediate"
            }
            input_df = create_df(input_ds, spark, output_version, project_id, project_name, logger)
            df_map.update({"df_" +input_ds_name: input_df})
    return df_map


def create_prepare_df(inputs, kwargs, project_id, project_name, output_version, logger):

    spark = kwargs['spark']()

    ds_list = kwargs.get("ds_conf")
    name_ds_map_dict = {}
    for ds in ds_list:
        name_ds_map_dict.update({ds.get("name"): ds})
    for input_ds_name in inputs:
        if input_ds_name in name_ds_map_dict.keys():
            input_df = create_df(name_ds_map_dict.get(input_ds_name), spark, output_version, project_id, project_name, logger)

        else:
            input_ds = {
                "name": input_ds_name,
                "version": output_version.split(","),
                "cat": "intermediate"
            }
            input_df = create_df(input_ds, spark, output_version, project_id, project_name, logger)

    return {"input_df": input_df}


def create_input_df(runtime, inputs, args, project_id, project_name, output_version, logger):
    df_choose = {
        "pyspark": readClickhouse(inputs, args, project_id, project_name, output_version, logger),
        "python3": readClickhouse(inputs, args, project_id, project_name, output_version, logger),
        "r": readClickhouse(inputs, args, project_id, project_name, output_version, logger),
        "sparkr": readClickhouse(inputs, args, project_id, project_name, output_version, logger),
        "prepare": create_prepare_df(inputs, args, project_id, project_name, output_version, logger)
    }

    df_map = df_choose.get(runtime)

    return df_map


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


def get_sample_df(output_id, project_id, df):

    table_name = "dataset"
    key = {
        "id": output_id,
        "projectId": project_id
    }
    dataset_item = get_dynamodb_item(table_name, key)
    sample = dataset_item.get("sample")
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

    return sample_df


def df_out(ph_conf, output_version, ch_client, df, project_ip, project_id,  table, output_id, mode="append", numPartitions = 2, database='default'):

    # 写入s3
    table_name = "_".join(table.split("_")[1:])
    path = f"s3://ph-platform/2020-11-11/lake/pharbers/{project_id}/{table_name}/"
    df.repartition(numPartitions).write.format("parquet") \
                .mode("append") \
                .partitionBy("version") \
                .save(path)

    # 先判断 clickhouse 中是否有数据
    sql = f"select count(*) from `{table}`"
    res = ch_client.execute(sql)
    count = res[0][0]
    if count == 0:
        # 进行sample 策略
        sample_df = get_sample_df(output_id, project_id, df)


        # 写入clickhouse
        sample_df.write.format("jdbc").mode(mode) \
            .option("url", f"jdbc:clickhouse://{project_ip}:8123/{database}") \
            .option("dbtable", f"`{table}`") \
            .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
            .option("user", "default") \
            .option("password", "") \
            .option("batchsize", 1000) \
            .option("socket_timeout", 300000) \
            .option("numPartitions", numPartitions) \
            .option("rewrtieBatchedStatements", True) \
            .save()
        putOutputSchema(output_id, project_id, sample_df, output_version)

        # 创建version表
        put_item_to_version(output_id, project_id, output_version, ph_conf.get("ownerId"))


def out_to_s3(df, ds_conf, logger):

    logger.debug("向s3写入数据")
    prop = ds_conf.get("prop")
    logger.debug(prop)
    logger.debug(type(prop))
    ds_format = prop.get("format")
    path = prop.get("path")
    partitions = prop.get("partitions")
    if ds_format == "Parquet":
        df.repartition(partitions).write.format("parquet") \
            .mode("append") \
            .save(path)
    elif ds_format == "CSV":
        df.repartition(partitions).write.format("csv")\
            .option("header", "true") \
            .mode("overwrite")\
            .save(path)


def addVersion(df, version, version_colname='version'):
    df = df.withColumn(version_colname, lit(version))
    return df


def deleteTableVersionSql(table, content, colname='version', database='default'):
    sql_content = f"ALTER TABLE {database}.`{table}` DELETE WHERE `{colname}`='{content}'"
    return sql_content


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


def put_item_to_version(output_id, project_id, output_version, owner):

    table_name = "version"
    version_item = {}
    version_item.update({"id": project_id + "_" + output_id})
    version_item.update({"projectId": project_id})
    version_item.update({"datasetId": output_id})
    version_item.update({"name": output_version})
    version_item.update({"date": str(int(round(time.time() * 1000)))})
    version_item.update({"owner": owner})

    put_dynamodb_item(table_name, version_item)


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

def changeIntToDouble(df):
    for colname,coltype in df.dtypes:
        if coltype == 'int':
            df = df.withColumn(colname, df[colname].cast('double'))
    return df


def createOutputs(args, ph_conf, outputs, outputs_id, project_id, project_name, output_version, logger):

    out_df = args.get("out_df")
    if out_df:

        out_df = changeIntToDouble(out_df)
        table_name = project_id + "_" + outputs[0]

        # 获取 project_ip
        project_ip = get_project_ip(project_id, project_name, logger)

        logger.debug(table_name)
        logger.debug(output_version)
        logger.debug(table_name)
        # 获取clickhouse_client
        ch_client = clickhouse_client(project_id, project_name, logger)

        add_version_df = addVersion(out_df, output_version, version_colname='version')
        logger.debug("df添加version完成")
        sql_create_table = createClickhouseTableSql(add_version_df, table_name)
        logger.debug(sql_create_table)
        logger.debug("根据df创建建表语句")

        ch_client.execute(sql_create_table)
        logger.debug("根据建表语句创建表成功")

        # sql_delete_version = deleteTableVersionSql(table_name, output_version)
        # logger.debug(sql_delete_version)
        # logger.debug("创建删除语句")
        # ch_client.execute(sql_delete_version)
        # logger.debug("根据删除语句删除成功")

        ds_list = args.get("ds_conf")
        output_name = outputs[0]
        name_ds_map_dict = {}
        for ds in ds_list:
            name_ds_map_dict.update({ds.get("name"): ds})
        if output_name in name_ds_map_dict.keys():
            logger.debug(name_ds_map_dict.get(output_name))
            logger.debug(type(name_ds_map_dict.get(output_name)))
            out_to_s3(add_version_df, name_ds_map_dict.get(output_name), logger)
        else:
            # 获取
            logger.debug("输出df的count")
            add_version_df.show(10)
            logger.debug(add_version_df.count())
            df_out(ph_conf, output_version, ch_client, add_version_df, project_ip, project_id, table_name, outputs_id[0])
            logger.debug("向创建的表写入数据成功")




@click.command()
@click.option('--owner')
@click.option('--dag_name')
@click.option('--run_id')
@click.option('--job_full_name')
@click.option('--job_id')
@click.option('--ph_conf')
def debug_execute(**kwargs):
    try:
        logger = phs3logger(kwargs["job_id"], LOG_DEBUG_LEVEL)
        args = {}
        args.update(kwargs)
        result = exec_before(**args)
        
        args.update(result if isinstance(result, dict) else {})
        result = execute(**args)

        args.update(result if isinstance(result, dict) else {})

        return result
    except Exception as e:
        logger = phs3logger(kwargs["job_id"])
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        raise e


if __name__ == '__main__':
    debug_execute()



