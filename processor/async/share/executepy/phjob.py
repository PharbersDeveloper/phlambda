# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""

import boto3
import json
import time
import re
from pyspark.sql.functions import lit
from datetime import datetime
from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL
from boto3.dynamodb.conditions import Key


# --写入路径
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



def execute(**kwargs):

    logger = phs3logger(kwargs["job_id"], LOG_DEBUG_LEVEL)
    spark = kwargs["spark"]()
    ph_share = json.loads(kwargs.get("ph_conf", {}))
    share = ph_share.get("share")
    shareProject = ph_share.get("tenantId")
    #owner = ph_share.get("owner")
    #showName = ph_share.get("showName")
    #projectName = ph_share.get("projectName")


    for item in share:
        company = item["company"]
        sourceProjectId = item["sourceProjectId"]
        datasetName = item["datasetName"]
        version = item["version"]
        logger.debug(f"share item: {item}")
        # 从s3 读取数据
        path = f"s3://ph-platform/2020-11-11/lake/{company}/{sourceProjectId}/{datasetName}/version={version}"
        df = spark.read.parquet(path)
        # 公有数据域
        #version_col = re.findall(pattern="version=(.*)", string=str(version))[0]
        share_path = f"s3://ph-platform/2020-11-11/lake/{company}/{shareProject}/{datasetName}"
        write_to_path(share_num=1, mode="overwrite", df=df, col_of_partitionBy=[str(version)], path_of_write=share_path)


    return {'out_df': {}}
