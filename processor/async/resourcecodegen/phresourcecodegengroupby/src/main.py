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
            "expressions":{
                           "params": {
                                   "globalCount": True,
                                    "preFilter": {
                                        "distinct": True,
                                        "enabled": False,
                                        "expr": ""
                                    },
                                    "computedColumns": [],
                                    "keys": ["pha"],
                                    "values": [
                                        {"column": "sales",

                                            "countDistinct": True,
                                            "min": True,
                                            "avg": True,
                                            "max": True,
                                            "count": True,
                                            "sum": True,
                                            "stddev": True,

                                            "last": True,
                                            "first": True,
                                            "firstLastNotNull": True,
                                            "orderColumn": "date",

                                            "concat": True,
                                            "concatSeparator": ",",
                                            "concatDistinct": True,

                                            "type": "string",
                                            "index": 0,


                                        },
                                         {"column": "units",

                                            "countDistinct": True,
                                            "min": True,
                                            "avg": True,
                                            "max": True,
                                            "count": True,
                                            "sum": True,
                                            "stddev": True,

                                            "last": True,
                                            "first": True,
                                            "firstLastNotNull": True,
                                            "orderColumn": "date",

                                            "concat": True,
                                            "concatSeparator": ",",
                                            "concatDistinct": True,

                                            "type": "string",
                                            "index": 0,


                                        },
                                        {
                                            "customName": "custom_aggr_1",
                                            "customExpr": "max('sales')/min('units')",
                                            "type": "double"
                                        }
                                    ],
                                    "postFilter": {
                                        "distinct": True,
                                        "enabled": False,
                                        "expr": ""
                                    }
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
    g_postFilter = params['postFilter']
    g_computedColumns = params['computedColumns']
    g_values = params['values']
    g_keys = params['keys']
    g_globalCount = params['globalCount']

    # 读取yaml文件
    template_yaml = open('template.yaml', 'r', encoding='utf-8').read()
    template_yaml = yaml.load(template_yaml, Loader=yaml.FullLoader)

    # 获取phjob.py 模板
    phjob_script = template_yaml['template']['phjob.py']['content'] \
                        .replace("$g_input$", str(g_input)) \
                        .replace("$g_preFilter$", str(g_preFilter)) \
                        .replace("$g_postFilter$", str(g_postFilter)) \
                        .replace("$g_computedColumns$", str(g_computedColumns)) \
                        .replace("$g_values$", str(g_values)) \
                        .replace("$g_keys$", str(g_keys)) \
                        .replace("$g_globalCount$", str(g_globalCount))

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

    toS3(phjob_script, g_projectName, g_flowVersion, g_scripts_name, "phjob.py")
    
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
