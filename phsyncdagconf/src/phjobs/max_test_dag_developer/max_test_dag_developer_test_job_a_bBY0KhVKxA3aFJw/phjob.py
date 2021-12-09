# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""

from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL


def execute(**kwargs):
    logger = phs3logger(kwargs["job_id"], LOG_DEBUG_LEVEL)

    result_path_prefix = kwargs["result_path_prefix"]
    spark = kwargs["spark"]()
    depends_path = kwargs["depends_path"]

    return {}
