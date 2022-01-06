# -*- coding: utf-8 -*-
"""alfredyang@pharbers.com.

This is job template for Pharbers Max Job
"""

from phcli.ph_logs.ph_logs import phs3logger, LOG_DEBUG_LEVEL


def execute(**kwargs):
    data_frame = kwargs.get("input_df")

    #  Filter Start
    kwargs["filter_kvs"] = [{'province': ['=', '山西省']}]
    filter_kvs = kwargs["filter_kvs"]  # array [{"key", ["opt", "val"]}]
    for item in filter_kvs:
        key = list(item.keys())[0]
        opt, val = list(item.values())[0]
        data_frame = data_frame.filter(f"`{key}` {opt} '{val}'")
    #  Filter End

    #  Select Start
    kwargs["select_cols"] = "*" if len(['province', 'doi', '标准规格']) == 0 else ['province', 'doi', '标准规格']
    select_cols = kwargs["select_cols"]  # array ["col"]
    data_frame = data_frame.select(select_cols)
    #  Select End

    #  Operation Null Start
    kwargs["operation_null_default"] = 'asfasf'
    default = kwargs.get("operation_null_default")  # string "default value"
    if default is None:
        data_frame = data_frame.dropna(how="any")
    else:
        data_frame = data_frame.fillna(default)
    #  Operation Null Start

    return {'out_df': data_frame}

