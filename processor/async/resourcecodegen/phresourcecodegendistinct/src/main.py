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
            "expressions": { "parmas": {
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
    projectId = args['projectId']
    dagName = args['dagName']
    flowVersion = args['flowVersion']
    projectName = args['projectName']
    args_scripts = args['script']
    output = args['script']['outputs']
    inputs = args['script']['inputs']
    input = inputs[0]
    runtime = args["steps"][0]['runtime']
    scripts_name = args['script']['jobName']
    
    distinct_args = args["steps"][0]["expressions"]["parmas"]
    args_preFilter = distinct_args['preFilter']
    args_postFilter = distinct_args['postFilter']
    distinct_key = distinct_args['keys']

    # 读取yaml文件
    template_yaml = open('template.yaml', 'r', encoding='utf-8').read()
    template_yaml = yaml.load(template_yaml, Loader=yaml.FullLoader)

    # 获取phjob.py 模板
    phjob_script = template_yaml['template']['phjob.py']['content'] \
                        .replace("$args_preFilter$", str(args_preFilter)) \
                        .replace("$args_postFilter$", str(args_postFilter)) \
                        .replace("$distinct_key$", str(distinct_key)) \
                        .replace("$input$", str(input))

    # 获取phmain.py 模板
    phmain_script = template_yaml['template']['phmain.py']['content'] \
                        .replace("$dagName$", f"'{dagName}'") \
                        .replace("$script_name$", f"'{scripts_name}'") \
                        .replace("$projectId$", f"'{projectId}'") \
                        .replace("$runtime$", f"'{runtime}'") \
                        .replace("$output$", f"'{output}'") \
                        .replace("$inputs$", str(inputs)) \
                        .replace("$project_name$", f"'{projectName}'")


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
    toS3(phmain_script, projectName, flowVersion, scripts_name, "phmain.py")
    
    return args['script']

