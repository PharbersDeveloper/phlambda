# -*- coding: utf-8 -*-

# 废弃
S3_PREFIX = "s3://"
CLI_VERSION = "2020-11-11"

AWS_REGION = "cn-northwest-1"

ASSUME_ROLE_ARN = "YXJuOmF3cy1jbjppYW06OjQ0NDYwMzgwMzkwNDpyb2xlL1BoLUJhY2stUlc="
ASSUME_ROLE_EXTERNAL_ID = "Ph-Back-RW"

# 废弃
TEMPLATE_BUCKET = "ph-platform"

# 针对低代码
LOW_CODE_TEMPLATE_OPERATOR = {
    "base_funcs": "/template/python/phcli/maxauto/base_funcs.tmp",
    "filter_on_value_for_pyspark": "/template/python/phcli/maxauto/filter_on_value_for_pyspark_dev.tmp",
    "filter_on_numerical_range_for_pyspark": "/template/python/phcli/maxauto/filter_on_numerical_range_for_pyspark_dev.tmp",
    "select_for_pyspark": "/template/python/phcli/maxauto/select_for_pyspark_dev.tmp",
    "remove_row_on_empty_for_pyspark": "/template/python/phcli/maxauto/remove_row_on_empty_for_pyspark_dev.tmp",
    "fill_empty_with_value_for_pyspark": "/template/python/phcli/maxauto/fill_empty_with_value_for_pyspark_dev.tmp",
    "column_replace_for_pyspark": "/template/python/phcli/maxauto/column_replace_for_pyspark_dev.tmp",
    "value_replace_for_pyspark": "/template/python/phcli/maxauto/value_replace_for_pyspark_dev.tmp"
}
