# -*- coding: utf-8 -*-

# 废弃
S3_PREFIX = "s3://"
CLI_VERSION = "2020-11-11"

ASSUME_ROLE_ARN = 'YXJuOmF3cy1jbjppYW06OjQ0NDYwMzgwMzkwNDpyb2xlL1BoLUNsaS1NYXhBdXRv'
ASSUME_ROLE_EXTERNAL_ID = 'Ph-Cli-MaxAuto'

# 废弃
TEMPLATE_BUCKET = "ph-platform"
DAGS_S3_BUCKET = 's3fs-ph-airflow'
DAGS_S3_PREV_PATH = 'airflow/dags/'
DAGS_S3_PHJOBS_PATH = '/jobs/python/phcli/'
DAGS_S3_LMD_PTAH = '/jobs/python/phcli/args_lmd/'

# 废弃
ENV_WORKSPACE_KEY = 'PH_WORKSPACE'
ENV_WORKSPACE_DEFAULT = '.'
ENV_CUR_PROJ_KEY = 'PH_CUR_PROJ'
ENV_CUR_PROJ_DEFAULT = '.'
ENV_CUR_IDE_KEY = 'PH_CUR_IDE'
ENV_CUR_IDE_DEFAULT = 'c9'
ENV_CUR_RUNTIME_KEY = 'PH_CUR_RUNTIME'
ENV_CUR_RUNTIME_DEFAULT = 'python3'

# Template 文件路径
# 废弃
TEMPLATE_PHCONF_FILE = "/template/python/phcli/maxauto/phconf-20210104.yaml"

# Python & pyspark
TEMPLATE_PHJOB_FILE_PY = "/template/python/phcli/maxauto/phjob-py_dev.tmp"
TEMPLATE_PHMAIN_FILE_PY = "/template/python/phcli/maxauto/phmain-py_dev.tmp"
# TEMPLATE_PHMAIN_FILE_PYTHON3 = "/template/python/phcli/maxauto/phmain-20220210.tmp"

# R & SparkR
TEMPLATE_PHMAIN_FILE_R = "/template/python/phcli/maxauto/phmain-r_dev.tmp"
TEMPLATE_PHJOB_FILE_R = "/template/python/phcli/maxauto/phjob-r_dev.tmp"

# 低代码 废弃
TEMPLATE_OPERATOR_FILTER_FILE_PY = "/template/python/phcli/maxauto/filter_for_pyspark_20211228.tmp"
TEMPLATE_OPERATOR_SELECT_FILE_PY = "/template/python/phcli/maxauto/select_for_pyspark_20211228.tmp"
TEMPLATE_OPERATOR_OPERATION_NULL_FILE_PY = "/template/python/phcli/maxauto/operation_null_for_pyspark_20211228.tmp"
TEMPLATE_OPERATOR_SCRIPT_FILE_PY = "/template/python/phcli/maxauto/script-20220331_dev.tmp"

# 废弃 Phcli 脚本
TEMPLATE_JUPYTER_PYTHON_FILE = '/template/python/phcli/maxauto/phJupyterPython-20210322.json'
TEMPLATE_JUPYTER_R_FILE = '/template/python/phcli/maxauto/phJupyterR-20210122.json'

# Airflow
# 废弃
TEMPLATE_PHDAG_FILE = "/template/python/phcli/maxauto/phdag-20210104.yaml"

TEMPLATE_PHGRAPHTEMP_FILE = "/template/python/phcli/maxauto/phGraphTemp_dev.tmp"
TEMPLATE_PHDAGJOB_FILE = "/template/python/phcli/maxauto/phDagJob_dev.tmp"
# TEMPLATE_PHPYTHON3DAGJOB_FILE = "/template/python/phcli/maxauto/phPython3DagJob-20220215.tmp"
# TEMPLATE_PHPYTHON3GRAPHTEMP_FILE = "/template/python/phcli/maxauto/phpython3temp-20220215.tmp"

# StepFunction
TEMPLATE_SFN_LMD_STEP_FILE = "/template/python/phcli/step_functions/step_tmp/ph-sfn-create-lmd-step-20210713.tmp"
TEMPLATE_SFN_STEP_FILE = "/template/python/phcli/step_functions/step_tmp/ph-sfn-create-step-20210713.tmp"
TEMPLATE_SFN_RUN_ID_STEP_FILE = "/template/python/phcli/step_functions/step_tmp/ph-sfn-create-run-id-20210716.tmp"
TEMPLATE_SFN_DAG_ARGS_STEP_FILE = "/template/python/phcli/step_functions/step_tmp/ph-sfn-create-dag-args-step-20210716.tmp"
TEMPLATE_SFN_PARALLEL_STEP_FILE = "/template/python/phcli/step_functions/step_tmp/ph-sfn-create-paraller-step-20210708.tmp"

# 废弃 Phcli
DEFAULT_RESULT_PATH_FORMAT_STR = "s3://{bucket_name}/{version}/{dag_name}/"
DEFAULT_RESULT_PATH_BUCKET = "ph-max-auto"
DEFAULT_RESULT_PATH_VERSION = "2020-08-11"
DEFAULT_RESULT_PATH_SUFFIX = "refactor/runs"
DEFAULT_ASSET_PATH_FORMAT_STR = "s3://{bucket_name}/{version}/"
DEFAULT_ASSET_PATH_BUCKET = 'ph-max-auto'
DEFAULT_ASSET_PATH_VERSION = "2020-08-11"
DEFAULT_ASSET_PATH_SUFFIX = "asset"

# 废弃 Phcli
DEFAULT_ROLE_ARN = 'arn:aws-cn:iam::444603803904:role/Pharbers-IoC-Maintainer'
DEFAULT_MACHINE_TYPE = 'STANDARD'
DEFAULT_MACHINE_ARN_SUFFIX = 'arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:'

# 针对Python Click模块
PRESET_MUST_ARGS = 'owner, dag_name, run_id, job_full_name, ph_conf'

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
