import pytest
import src.main as app


class TestGenerateCode:
    def test_generate(self):
        event = {
            "traceId": "alex_test_traceId",
            "tenantId": "zudIcG_17yj8CEUoCTHg",
            "projectId": "4pzAo3zNFF-gIrUQw9t1",
            "projectName": "Tutorial",
            "flowVersion": "developer",
            "dagName": "Tutorial",
            "owner": "5UBSLZvV0w9zh7-lZQap",
            "showName": "鹏钱",
            "script": {
                "jobName": "compute_joinab",
                "runtime": "join",
                "jobPath": "",
                "inputs": ["A", "B"],      # 现在没用，可能以后有用
                "outputs": ["joinab"],            # 现在没用，可能以后有用
                "id": "001"
            },
            "steps": [                  # 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
                {
                    "id": "4pzAo3zNFF-gIrUQw9t1_B98WIHKrXjUmTQa",
                    "pjName": "4pzAo3zNFF-gIrUQw9t1_Tutorial_Tutorial_developer_compute_joinab",
                    "stepId": "1",
                    "index": "1",
                    "runtime": "join",
                    "stepName": "Initial Filter On Value",
                    "ctype": "Join",
                    "groupIndex": 0,
                    "groupName": "",
                    "expressionsValue": "JSON",
                    "expressions": {
                        "params": {
                            "preFilters": [
                                {
                                    "ds": "B",
                                    "index": 0,
                                    "preFilter": {
                                        "distinct": False,
                                        "enabled": True,
                                        "expr": "`名称` like '%$fruit%'"
                                    }
                                },
                                {
                                    "ds": "A",
                                    "index": 1,
                                    "preFilter": {
                                        "distinct": False,
                                        "enabled": True,
                                        "expr": "`姓名` like '%$name%'"
                                    }
                                }
                            ],
                            "preJoinComputedColumns": [
                                {
                                    "ds": "B",
                                    "index": 0,
                                    "computedColumns": []
                                },
                                {
                                    "ds": "A",
                                    "index": 1,
                                    "computedColumns": []
                                }
                            ],
                            "joins": [
                                {
                                    "datasets": [
                                        {
                                            "name": "B",
                                            "index": 0
                                        },
                                        {
                                            "name": "A",
                                            "index": 1
                                        }
                                    ],
                                    "normalizeText": False,
                                    "type": "LEFT",
                                    "caseInsensitive": False,
                                    "on": [
                                        {
                                            "type": "=",
                                            "conditions": [
                                                {
                                                    "ds": "B",
                                                    "column": "序号"
                                                },
                                                {
                                                    "ds": "A",
                                                    "column": "ID"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "selectedColumns": [
                                {
                                    "ds": "B",
                                    "index": 0,
                                    "prefix": "",
                                    "type": "select",
                                    "columns": [
                                        "序号",
                                        "名称",
                                        "重量",
                                        "单价",
                                        "总价",
                                        "损耗成本",
                                        "利润",
                                        "产地",
                                        "运输方式"
                                    ]
                                },
                                {
                                    "ds": "A",
                                    "index": 1,
                                    "prefix": "",
                                    "type": "select",
                                    "columns": [
                                        "姓名",
                                        "ID",
                                        "学号",
                                        "成绩",
                                        "籍贯",
                                        "年龄"
                                    ]
                                }
                            ],
                            "postJoinComputedColumns": [],
                            "postFilter": {
                                "distinct": False,
                                "enabled": False,
                                "expr": ""
                            }
                        }
                    }
                },
            ]
        }

        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()


