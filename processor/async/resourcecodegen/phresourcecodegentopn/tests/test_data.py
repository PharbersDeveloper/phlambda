import json
import pytest
import src.main as app


class TestGenerateCode:
    def test_generate(self):
        event = {
            "traceId": "alex-traceid",
            "projectId": "ggjpDje0HUC2JW",
            "projectName": "demo",
            "flowVersion": "developer",
            "dagName": "demo",
            "owner": "5UBSLZvV0w9zh7-lZQap",
            "showName": "鹏钱",
            "script": {
                "id": "y68cqkuoE2rESML",
                "jobName": "compute_t2",
                "jobPath": "",
                "inputs": [
                    "水果"
                ],
                "outputs": [
                    "t2"
                ],
                "runtime": "topn"
            },
            "steps": [
                {
                    "pjName": "ggjpDje0HUC2JW_demo_demo_developer_compute_t2",
                    "stepId": "1",
                    "ctype": "TopN",
                    "expressions": {
                        "type": "topn",
                        "code": "pyspark",
                        "params": {
                            "firstRows": 18,
                            "lastRows": 11,
                            "keys": [],
                            "preFilter": {
                                "distinct": False,
                                "enabled": True,
                                "expression": "`名称` like '%$fruit%'"
                            },
                            "orders": [
                                {
                                    "column": "利润",
                                    "desc": False
                                }
                            ],
                            "denseRank": False,
                            "duplicateCount": False,
                            "rank": False,
                            "rowNumber": False,
                            "retrievedColumns": [],
                            "computedColumns": []
                        }
                    },
                    "expressionsValue": "JSON",
                    "groupIndex": 0,
                    "groupName": "",
                    "id": "ggjpDje0HUC2JW_y68cqkuoE2rESML",
                    "index": "1",
                    "runtime": "topn",
                    "stepName": "topn"
                }
            ],
            "notification": {
                "required": True
            },
            "oldImage": [
            ],
            "ifsteps": 1
        }

        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()


