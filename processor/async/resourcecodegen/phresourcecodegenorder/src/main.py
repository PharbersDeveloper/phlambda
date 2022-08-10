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
                                        "distinct": False,
                                        "enabled": True,
                                        "expression": "`city` = '长春市'"
                                    },
                                    "orders": [
                                        {"column": "year", "desc": True},
                                        {"column": "month", "desc": False}
                                    ],
                                    "denseRank": True,
                                    "rank": True,
                                    "rowNumber": True,
                                    "computedColumns": [
                                        {
                                            "expr": "concat(pha, city)",
                                            "name": "AAA",
                                            "type": "string"
                                        }
                                    ]
                                }
                        }
            }
    ]
}
'''


def lambda_handler(event, context):
    args = event
    flowVersion = args['flowVersion']
    projectName = args['projectName']
    output = args['script']['outputs']
    input = args['script']['inputs'][0]
    scripts_name = args['script']['jobName']

    params = args["steps"][0]["expressions"]["params"]
    args_preFilter = params['preFilter']
    args_orders = params['orders']
    args_denseRank = params['denseRank']
    args_rank = params['rank']
    args_rowNumber = params['rowNumber']
    args_computedColumns = params['computedColumns']

    # 读取yaml文件
    template_yaml = open('template.yaml', 'r', encoding='utf-8').read()
    template_yaml = yaml.load(template_yaml, Loader=yaml.FullLoader)

    # 获取phjob.py 模板
    phjob_script = template_yaml['template']['phjob.py']['content'] \
        .replace("$project_id$", event["projectId"]) \
        .replace("$job_id$", event["steps"][0]["id"].split("_")[-1]) \
        .replace("$input$", str(input)) \
        .replace("$args_preFilter$", str(args_preFilter)) \
        .replace("$args_orders$", str(args_orders)) \
        .replace("$args_denseRank$", str(args_denseRank)) \
        .replace("$args_rank$", str(args_rank)) \
        .replace("$args_rowNumber$", str(args_rowNumber)) \
        .replace("$args_computedColumns$", str(args_computedColumns))

    job_file_name = "phjob.py"
    project_folder_name = f"{projectName}_{projectName}_{flowVersion}"
    job_folder_name = f"{projectName}_{projectName}_{flowVersion}_{scripts_name}"
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
