# -*- coding: utf-8 -*-
import os

import click
import traceback
from phjob import execute
from pyspark.sql import SparkSession
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL

# 获取Spark实例
os.environ["PYSPARK_PYTHON"] = "python3"
spark = SparkSession.builder.master("yarn")
default_config = {
    "spark.sql.codegen.wholeStage": False,
    "spark.sql.execution.arrow.pyspark.enabled": "true",
}
for k, v in default_config.items():
    spark = spark.config(k, v)
spark = spark.enableHiveSupport().getOrCreate()
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
if access_key is not None:
    spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
    spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
    spark._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
    spark._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.cn-northwest-1.amazonaws.com.cn")

@click.command()
@click.option('--owner')
@click.option('--dag_name')
@click.option('--run_id')
@click.option('--job_full_name')
@click.option('--job_id')
@click.option('--ph_conf')
@click.option('--tenant_ip')
def debug_execute(**kwargs):
    logger = phs3logger("emr_log", LOG_DEBUG_LEVEL)
    try:
        args = {}
        args.update(kwargs)
        args.update({"spark": spark})

        result = execute(**args)

        args.update(result if isinstance(result, dict) else {})

        return result
    except Exception as e:
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        raise e

if __name__ == '__main__':
    debug_execute()

