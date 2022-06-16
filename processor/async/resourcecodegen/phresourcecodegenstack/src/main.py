import json
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
                        .replace("$g_inputs$", str(g_inputs)) \
                        .replace("$g_preFilter$", str(g_preFilter)) \
                        .replace("$g_postFilter$", str(g_postFilter)) \
                        .replace("$g_selectedColumns$", str(g_selectedColumns)) \
                        .replace("$g_columnsMatches$", str(g_columnsMatches)) \
                        .replace("$g_originColumn$", str(g_originColumn))

    # 写出到s3
    def getScriptPathKey(g_projectName, g_flowVersion, g_output):
        return f"2020-11-11/jobs/python/phcli/{g_projectName}_{g_projectName}_{g_flowVersion}/{g_projectName}_{g_projectName}_{g_flowVersion}_{g_output}"

    def toS3(script, g_projectName, g_flowVersion, g_scripts_name, filename):
        script_bytes = str.encode(script)
        client = boto3.client('s3')
        response = client.put_object(
            Body = script_bytes,
            Bucket='ph-platform',
            Key=f"{getScriptPathKey(g_projectName, g_flowVersion, g_scripts_name)}/{filename}") 

    #toS3(phjob_script, g_projectName, g_flowVersion, g_scripts_name, "phjob.py")
    
    with open("phjob_tt.py", "w") as file:
        file.write(phjob_script)
    
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

lambda_handler(event, context="")