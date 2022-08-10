import os
import yaml
import boto3

'''

args:

event = { 
    "traceId": "alfred-resource-creation-traceId",
    "projectId": "ggjpDje0HUC2JW",
    "projectName": "demo",
    "flowVersion": "developer",
    "dagName": "demo",
    "owner": "hbzhao",
    "showName": "赵浩博",
    "script": {
        "jobName": "compute_BB",
        "runtime": "topn",
        "jobPath": "",
        "inputs": ["AA"],           #// 现在没用，可能以后有用
        "outputs": "yyw",            #// 现在没用，可能以后有用
        "id": "001"
    },
    "steps": [                  #// 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
        {
            "id": "alextest_demo_demo_developer_compute_十多个",
            "stepId": "1",
            "index": "1",
            "runtime": "topn",
            "stepName": "Initial Filter On Value",
            "ctype": "FillEmptyWithValue",
            "groupIndex": 0,
            "groupName": "",
            "expressionsValue": "JSON",
            "expressions":{
                            "params" : {
                                "preFilter": {
                                    "distinct": True,
                                    "enabled": True,
                                    "expr": "`year`='2018'"
                                },
                                "computedColumns":  [

                                ],
                                "identifiers": ["city", "pha"],
                                "pivot": {   
                                    "globalCount": True,
                                    "keyColumns": ["brand", "year"],
                                    "topnLimit": 20, #// 暂时不做
                                    "minOccLimit": 1, #// 暂时不做
                                    "explicitValues": ["预留参数，暂时不做"],
                                    "valueColumns": [
                                        {
                                            "avg": False,
                                            "column": "sales",
                                            "concat": False,
                                            "concatDistinct": False,
                                            "concatSeparator": ",",
                                            "count": False,
                                            "countDistinct": False,
                                            "first": False,
                                            "firstLastNotNull": False,
                                            "last": False,
                                            "max": True,
                                            "min": True,
                                            "orderColumn": "11111",
                                            "stddev": False,
                                            "sum": False
                                        },
                                        {
                                            "avg": False,
                                            "column": "units",
                                            "concat": False,
                                            "concatDistinct": False,
                                            "concatSeparator": ",",
                                            "count": False,
                                            "countDistinct": False,
                                            "first": False,
                                            "firstLastNotNull": False,
                                            "last": False,
                                            "max": True,
                                            "min": True,
                                            "orderColumn": "11111",
                                            "stddev": False,
                                            "sum": False
                                        }
                                    ]
                                },
                                "otherColumns": [
                                    {
                                        "avg": False,
                                        "column": "year",
                                        "concat": True,
                                        "concatDistinct": True,
                                        "concatSeparator": ",",
                                        "count": False,
                                        "countDistinct": True,
                                        "first": False,
                                        "firstLastNotNull": False,
                                        "last": False,
                                        "orderColumn": "11111",
                                        "max": False,
                                        "min": False,
                                        "stddev": False,
                                        "sum": False
                                    },
                                    {
                                        "avg": False,
                                        "column": "brand",
                                        "concat": True,
                                        "concatDistinct": True,
                                        "concatSeparator": ",",
                                        "count": False,
                                        "countDistinct": True,
                                        "first": False,
                                        "firstLastNotNull": False,
                                        "last": False,
                                        "orderColumn": "11111",
                                        "max": False,
                                        "min": False,
                                        "stddev": False,
                                        "sum": False
                                    },
                                    {
                                        "avg": False,
                                        "column": "pha",
                                        "concat": True,
                                        "concatDistinct": True,
                                        "concatSeparator": ",",
                                        "count": False,
                                        "countDistinct": True,
                                        "first": True,
                                        "firstLastNotNull": False,
                                        "last": False,
                                        "orderColumn": "date",
                                        "max": False,
                                        "min": False,
                                        "stddev": False,
                                        "sum": False
                                    }
                                ]
                            }
                        }
            }
    ]
}

'''


def lambda_handler(event, context):
    g_flowVersion = event['flowVersion']
    g_projectName = event['projectName']
    g_output = event['script']['outputs']
    g_input = event['script']['inputs'][0]
    g_scripts_name = event['script']['jobName']

    params = event["steps"][0]["expressions"]["params"]
    g_preFilter = params['preFilter']
    g_computedColumns = params['computedColumns']
    g_identifiers = params['identifiers']
    g_pivot = params['pivot']
    g_otherColumns = params['otherColumns']

    # 读取yaml文件
    template_yaml = open('template.yaml', 'r', encoding='utf-8').read()
    template_yaml = yaml.load(template_yaml, Loader=yaml.FullLoader)

    # 获取phjob.py 模板
    phjob_script = template_yaml['template']['phjob.py']['content'] \
        .replace("$project_id$", event["projectId"]) \
        .replace("$job_id$", event["steps"][0]["id"].split("_")[-1]) \
        .replace("$g_input$", str(g_input)) \
        .replace("$g_preFilter$", str(g_preFilter)) \
        .replace("$g_computedColumns$", str(g_computedColumns)) \
        .replace("$g_identifiers$", str(g_identifiers)) \
        .replace("$g_pivot$", str(g_pivot)) \
        .replace("$g_otherColumns$", str(g_otherColumns))

    job_file_name = "phjob.py"
    project_folder_name = f"{g_projectName}_{g_projectName}_{g_flowVersion}"
    job_folder_name = f"{g_projectName}_{g_projectName}_{g_flowVersion}_{g_scripts_name}"
    s3_path = f'{os.environ["CLI_VERSION"]}{os.environ["DAG_S3_JOBS_PATH"]}/{project_folder_name}/{job_folder_name}'

    def toS3(code, bucket, path):
        client = boto3.client("s3")
        client.put_object(Body=str.encode(code), Bucket=bucket, Key=f"{path}/{job_file_name}")
        client.put_object(Body=str.encode(""), Bucket=bucket, Key=f"{path}/{event['traceId']}")
    toS3(phjob_script, os.environ["BUCKET"], s3_path)

    return {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {
                "script": event["script"]["jobName"]
            },
            "error": {}
        }
    }
