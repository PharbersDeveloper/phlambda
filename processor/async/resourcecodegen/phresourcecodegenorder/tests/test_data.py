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
                "jobName": "compute_sorta",
                "runtime": "sort",
                "jobPath": "",
                "inputs": ["A"],  # 现在没用，可能以后有用
                "outputs": ["sorta"],  # 现在没用，可能以后有用
                "id": "001"
            },
            "steps": [  # 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
                {
                    "id": "4pzAo3zNFF-gIrUQw9t1_JfMiCR8JeAil162",
                    "pjName": "4pzAo3zNFF-gIrUQw9t1_Tutorial_Tutorial_developer_compute_sorta",
                    "stepId": "1",
                    "index": "1",
                    "runtime": "pivot",
                    "stepName": "pivot",
                    "ctype": "Pivot",
                    "groupIndex": 0,
                    "groupName": "",
                    "expressionsValue": "JSON",
                    "expressions": {
                        "type": "sort",
                        "code": "pyspark",
                        "params": {
                            "preFilter": {
                                "distinct": False,
                                "enabled": True,
                                "expression": "`姓名` like '%$name%'"
                            },
                            "orders": [
                                {
                                    "column": "ID",
                                    "desc": False
                                }
                            ],
                            "denseRank": True,
                            "rank": True,
                            "rowNumber": True,
                            "computedColumns": []
                        }
                    }
                },
            ]
        }

        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()
