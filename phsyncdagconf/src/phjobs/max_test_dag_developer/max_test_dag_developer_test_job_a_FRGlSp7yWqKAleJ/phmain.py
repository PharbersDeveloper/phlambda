# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""
import os
import json
import click
import traceback
from phjob import execute
from phcli.ph_logs.ph_logs import phs3logger
from phcli.ph_max_auto.ph_hook.ph_hook import exec_before, exec_after


def readClickhouse(inputs, kwargs):
    df_map = {}
    spark = kwargs['spark']()
    version_map = json.loads(kwargs.get("version"))
    for dbtable in inputs:
        version = version_map.get(dbtable)
        df = spark.read.format("jdbc") \
            .option("url", "jdbc:clickhouse://192.168.16.117:8123") \
            .option("dbtable", dbtable) \
            .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
            .option("user", "default") \
            .option("password", "") \
            .option("fetchsize", "500000").load()
        df = df.where(df.version==version).drop('version')
        df_map.update({"df_" + dbtable: df})
    return df_map

@click.command()
@click.option('--owner')
@click.option('--dag_name')
@click.option('--run_id')
@click.option('--job_full_name')
@click.option('--job_id')
@click.option('--测试DS_001')
@click.option('--测试DS_002')
@click.option('--测试DS_003')
def debug_execute(**kwargs):
    try:
        args = {"name": "max_test_dag_developer_test_job_a_FRGlSp7yWqKAleJ"}
        inputs = ["测试ds_001", "测试ds_002"] 
        outputs = ["测试ds_003"]
        args.update({"input_datasets": inputs})
        df_map = readClickhouse(inputs, kwargs)

        args.update(df_map)
        result = exec_before(**args)

        args.update(result if isinstance(result, dict) else {})
        result = execute(**args)

        args.update(result if isinstance(result, dict) else {})
        result = exec_after(outputs=outputs, **args)

        return result
    except Exception as e:
        logger = phs3logger(kwargs["job_id"])
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        raise e



if __name__ == '__main__':
    online_debug_execute()


