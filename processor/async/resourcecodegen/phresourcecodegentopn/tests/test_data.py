import json
import pytest
import src.main as app


class TestGenerateCode:
    def test_generate(self):
        event = {
            "traceId": "alex_test_traceId",
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
                "inputs": ["A"],      # 现在没用，可能以后有用
                "outputs": [],            # 现在没用，可能以后有用
                "id": "001"
            },
            "steps": [                  # 这个地方特别需要注意，直接传最后需要保存的样子，（跳出删除修改插入的思想死循环）
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
                    "expressions": {
                        "preFilter": {
                            "distinct": False,
                            "enabled": False,
                            "expression": ""
                        },
                        "computedColumns": [],
                        "retrievedColumns": [],
                        "firstRows": 1,
                        "lastRows": 1,
                        "keys": ["州省"],
                        "orders": [
                            {"column": "州省", "desc": True},
                            {"column": "总费用", "desc": False}
                        ],
                        "denseRank": True,
                        "duplicateCount": True,
                        "rank": True,
                        "rowNumber": True
                    }
                },
            ]
        }

        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()


