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
                "jobName": "compute_stackab",
                "runtime": "stack",
                "jobPath": "",
                "inputs": ["B", "A"],  # 现在没用，可能以后有用
                "outputs": ["stackab"],  # 现在没用，可能以后有用
                "id": "001"
            },
            "steps": [  # 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
                {
                    "id": "4pzAo3zNFF-gIrUQw9t1_jdLzuYvJT1lsXud",
                    "pjName": "4pzAo3zNFF-gIrUQw9t1_Tutorial_Tutorial_developer_compute_stackab",
                    "stepId": "1",
                    "index": "1",
                    "runtime": "distinct",
                    "stepName": "distinct",
                    "ctype": "Distinct",
                    "groupIndex": 0,
                    "groupName": "",
                    "expressionsValue": "JSON",
                    "expressions": {
                        "type": "stack",
                        "code": "pyspark",
                        "params": {
                            "preFilters": [
                                {
                                    "ds": "B",
                                    "index": 0,
                                    "preFilter": {
                                        "distinct": False,
                                        "enabled": True,
                                        "expr": "`序号` like '%$number%'"
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
                            "selectedColumns": [
                                "堆叠序号姓名"
                            ],
                            "columnsMatches": [
                                {
                                    "ds": "B",
                                    "columns": [
                                        "序号"
                                    ]
                                },
                                {
                                    "ds": "A",
                                    "columns": [
                                        "姓名"
                                    ]
                                }
                            ],
                            "originColumn": {
                                "enabled": False,
                                "columnName": "provider",
                                "originDatasets": [
                                    {
                                        "ds": "B",
                                        "value": "B"
                                    },
                                    {
                                        "ds": "A",
                                        "value": "A"
                                    }
                                ]
                            },
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
