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
            "expressions": { "params": {
                                "keys": ["city_tier_2010"],
                                "preFilter": {
                                    "distinct": False,
                                    "enabled": True,
                                    "expression": "`brand` LIKE '人血白蛋白' and `city` = '济南市'"
                                },
                                "postFilter": {
                                    "distinct": False,
                                    "enabled": False,
                                    "expression": ""
                                },
                                "globalCount": True
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
    g_input = args['script']['inputs'][0]
    scripts_name = args['script']['jobName']
    
    distinct_args = args["steps"][0]["expressions"]["params"]
    g_preFilter = distinct_args['preFilter']
    g_postFilter = distinct_args['postFilter']
    g_distinct_key = distinct_args['keys']
    g_globalCount = distinct_args['globalCount']

    # 读取yaml文件
    template_yaml = open('template.yaml', 'r', encoding='utf-8').read()
    template_yaml = yaml.load(template_yaml, Loader=yaml.FullLoader)

    # 获取phjob.py 模板
    phjob_script = template_yaml['template']['phjob.py']['content'] \
                        .replace("$g_preFilter$", str(g_preFilter)) \
                        .replace("$g_postFilter$", str(g_postFilter)) \
                        .replace("$g_distinct_key$", str(g_distinct_key)) \
                        .replace("$g_globalCount$", str(g_globalCount)) \
                        .replace("$g_input$", str(g_input))
    
    # 写出到s3
    def getScriptPathKey(projectName, flowVersion, output):
        return f"2020-11-11/jobs/python/phcli/{projectName}_{projectName}_{flowVersion}/{projectName}_{projectName}_{flowVersion}_{output}"

    def toS3(script, projectName, flowVersion, scripts_name, filename):
        script_bytes = str.encode(script)
        client = boto3.client('s3')
        response = client.put_object(
            Body = script_bytes,
            Bucket='ph-platform',
            Key=f"{getScriptPathKey(projectName, flowVersion, scripts_name)}/{filename}") 

    toS3(phjob_script, projectName, flowVersion, scripts_name, "phjob.py")
    
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

