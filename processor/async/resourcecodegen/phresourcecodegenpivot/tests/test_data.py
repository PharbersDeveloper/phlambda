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
                "jobName": "compute_pivota",
                "runtime": "stack",
                "jobPath": "",
                "inputs": ["A"],  # 现在没用，可能以后有用
                "outputs": ["pivota"],  # 现在没用，可能以后有用
                "id": "001"
            },
            "steps": [  # 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
                {
                    "id": "4pzAo3zNFF-gIrUQw9t1_iIjgaoWObCud1o1",
                    "pjName": "4pzAo3zNFF-gIrUQw9t1_Tutorial_Tutorial_developer_compute_pivota",
                    "stepId": "1",
                    "index": "1",
                    "runtime": "pivot",
                    "stepName": "pivot",
                    "ctype": "Pivot",
                    "groupIndex": 0,
                    "groupName": "",
                    "expressionsValue": "JSON",
                    "expressions": {
                        "type": "pivot",
                        "code": "pyspark",
                        "params": {
                            "preFilter": {
                                "distinct": False,
                                "enabled": True,
                                "expr": "`姓名` like '%$name%'"
                            },
                            "computedColumns": [],
                            "identifiers": [],
                            "pivot": {
                                "globalCount": True,
                                "keyColumns": [
                                    "姓名"
                                ],
                                "pivotedColumnType": "all",
                                "topnLimit": 0,
                                "minOccLimit": 0,
                                "explicitValues": [],
                                "valueColumns": []
                            },
                            "otherColumns": []
                        }
                    }
                },
            ]
        }

        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()
