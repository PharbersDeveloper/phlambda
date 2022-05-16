from updatesteps import *

'''
这个函数只做一件事情，将step写入数据库，然后将原有的数据写入oldimage
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
            "jobName": "compute_测试ds",
        }
        "steps": [ // 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
            {
                "id": "alextest_demo_demo_developer_compute_十多个",
                "stepId": "1",
                "index": "1",
                "runtime": "prepare",
                "stepName": "Initial Filter On Value",
                "ctype": "FillEmptyWithValue",
                "groupIndex": 0,
                "groupName": "",
                "expressionsValue": "JSON",
                "expressions": {
                    "type": "FillEmptyWithValue",
                    "code": "pyspark",
                    "params": {
                        "columns": ["订单内件数"],
                        "value": "4"
                    }
                }
            },
        ],
        "oldImage": [
            // 这个地方特别需要注意，保存steps修改前数据库的样子
        ]
    }

return = [
    {
        "id": "alextest_demo_demo_developer_compute_十多个",
        "stepId": "1",
        "index": "1",
        "runtime": "prepare",
        "stepName": "Initial Filter On Value",
        "ctype": "FillEmptyWithValue",
        "groupIndex": 0,
        "groupName": "",
        "expressionsValue": "JSON",
        "expressions": {
            "type": "FillEmptyWithValue",
            "code": "pyspark",
            "params": {
                "columns": ["订单内件数"],
                "value": "4"
            }
        }
    },
]
'''


def lambda_handler(event, context):
    # 差脚本名字（或者自己拼）
    name = f"{event['projectName']}_{event['dagName']}_{event['flowVersion']}"
    job_full_name = f"""{name}_{event["script"]["jobName"]}"""

    # 1 收集参数，转成想要的结构
    conf = {
        "steps": event["steps"],
        "traceId": event["traceId"],
        "projectId": event["projectId"],
        "jobFullName": job_full_name,
    }

    # 覆盖更新step表的数据
    old_steps = update_steps(conf)
    event["oldImage"] = old_steps

    return event["steps"]
