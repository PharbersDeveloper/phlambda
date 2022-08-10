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
        "inputs": ["df1", "df2"],           #// 现在没用，可能以后有用
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
                            "params": {
                                    "preFilters": [
                                        {
                                            "ds": "df1",
                                            "preFilter":
                                            {
                                            "distinct": True,
                                            "enabled": True,
                                            "expr": "`province`='吉林省'"
                                                }
                                        },
                                        {
                                            "ds": "df2",
                                            "preFilter":
                                            {
                                            "distinct": True,
                                            "enabled": False,
                                            "expr": "`province`='吉林省'"
                                            }
                                        }
                                    ],



                                "selectedColumns": ["city", "province", "sales", "hospital", "name"],
                                "columnsMatches": [
                                            { "ds": "df1", "columns": ["city", "province", "sales", "hospital", "name"] },
                                            { "ds": "df2", "columns": ["city", "province", "sales", None, None] }
                                                ],
                                "originColumn": {
                                "enabled": True,
                                "columnName": "original_dataset",
                                "originDatasets": [
                                { "ds": "df1", "value": "df1" },
                                { "ds": "df2", "value": "df2" }
                                                ]
                                },
                                "postFilter": { "distinct": True, "enabled": False, "expr": " `city`='长春市'" }

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
    g_inputs = event['script']['inputs']
    g_scripts_name = event['script']['jobName']

    params = event["steps"][0]["expressions"]["params"]
    g_preFilter = params['preFilters']
    g_selectedColumns = params['selectedColumns']
    g_columnsMatches = params['columnsMatches']
    g_originColumn = params['originColumn']
    g_postFilter = params['postFilter']

    # 读取yaml文件
    template_yaml = open('template.yaml', 'r', encoding='utf-8').read()
    template_yaml = yaml.load(template_yaml, Loader=yaml.FullLoader)

    # 获取phjob.py 模板
    phjob_script = template_yaml['template']['phjob.py']['content'] \
        .replace("$project_id$", event["projectId"]) \
        .replace("$job_id$", event["steps"][0]["id"].split("_")[-1]) \
        .replace("$g_inputs$", str(g_inputs)) \
        .replace("$g_preFilter$", str(g_preFilter)) \
        .replace("$g_postFilter$", str(g_postFilter)) \
        .replace("$g_selectedColumns$", str(g_selectedColumns)) \
        .replace("$g_columnsMatches$", str(g_columnsMatches)) \
        .replace("$g_originColumn$", str(g_originColumn))

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
