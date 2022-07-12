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


'''
args = {
    "common": {
        "tranceId": "",
        "runnerId": "sample_sample_developer_2022-07-04T05:49:39+00:00",
        "projectId": "Dp10sMiAYXWxRZj",
        "projectName": "sample",
        "owner": "16dc4eb5-5ed3-4952-aaed-17b3cc5f638b",
        "showName": "赵浩博",
        "tenantId": "zudIcG_17yj8CEUoCTHg"
    },
    "shares": [
        {
            "target": "ds name", // 共享时的目标DS 名称
            "targetCat": "catalog | intermediate | uploaded", // 共享时的目标DS的类型  catalog是数据目录  intermediate是结果数据集  uploaded 是上传的数据 都需要分别处理
            "targetPartitionKeys": [
                {
                    "name": "key1",
                    "type": "string"
                },
                {
                    "name": "key2",
                    "type": "string"
                }
            ],
            "sourceSelectVersions": ["version1", "version2", "version3"]
            "source": "ds name", // 共享时的源DS 名称
        }
    ]
}
'''




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

    logger = phs3logger(kwargs["job_id"], LOG_DEBUG_LEVEL)
    spark = kwargs["spark"]()
    ph_share = json.loads(kwargs.get("ph_conf", {}))
    shares = ph_share.get("shares")
    tenantId = ph_share.get("tenantId")
    company = ph_share.get("company")
    sourceProjectId = ph_share.get("projectId")
    #showName = ph_share.get("showName")
    #projectName = ph_share.get("projectName")


    for shareItem in shares:
        sourcePath = f"s3://ph-platform/2020-11-11/lake/{company}/{sourceProjectId}/{shareItem['source']}"
        #---- get df ------#
        df = spark.read.parquet(sourcePath)
        df = df.where(df["version"].isin(shareItem["sourceSelectVersions"]))

        #---- target Path -----------#
        if shareItem["targetCat"] == "catalog":
            targetPath = f"s3://ph-platform/2020-11-11/lake/{company}/{tenantId}/{shareItem['target']}"
            partitionByCols = [x["name"] for x in shareItem['targetPartitionKeys']]

            #---- get schema of target table --------------------#
            targetDsItem = get_ds_with_index(dsName=shareItem["target"], projectId=sourceProjectId)
            targetSchema = json.loads(targetDsItem["schema"]) if isinstance(targetDsItem["schema"], str) else targetDsItem["schema"]

            if len(targetSchema) == 0:
                write_to_path(share_num=1, mode="overwrite", df=df, col_of_partitionBy=partitionByCols, path_of_write=targetPath)
            else:
                write_to_path(share_num=1, mode="append", df=df, col_of_partitionBy=partitionByCols, path_of_write=targetPath)

        #TODO intermediate ,uploaded 如果需要后续添加处理逻辑

    return {'out_df': {}}
