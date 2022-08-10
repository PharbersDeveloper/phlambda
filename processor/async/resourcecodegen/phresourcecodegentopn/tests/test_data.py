import json
import pytest
import src.main as app


class TestGenerateCode:
    def test_generate(self):
        event = {
            "traceId": "alex-traceid",
            "tenantId": "zudIcG_17yj8CEUoCTHg",
            "projectId": "4pzAo3zNFF-gIrUQw9t1",
            "projectName": "Tutorial",
            "flowVersion": "developer",
            "dagName": "Tutorial",
            "owner": "5UBSLZvV0w9zh7-lZQap",
            "showName": "鹏钱",
            "script": {
                "id": "",
                "jobName": "compute_tpn",
                "jobPath": "",
                "inputs": [
                    "A"
                ],
                "outputs": [
                    "tpn"
                ],
                "runtime": "topn"
            },
            "steps": [
                {
                    "pjName": "4pzAo3zNFF-gIrUQw9t1_Tutorial_Tutorial_developer_compute_tpn",
                    "stepId": "1",
                    "ctype": "TopN",
                    "expressions": {
                        "type": "topn",
                        "code": "pyspark",
                        "params": {
                            "firstRows": 1,
                            "lastRows": 0,
                            "keys": [],
                            "preFilter": {
                                "distinct": False,
                                "enabled": True,
                                "expression": "`姓名` like '%$name%' and `学号` like '%$student_number%'"
                            },
                            "orders": [
                                {
                                    "column": "学号",
                                    "desc": False
                                }
                            ],
                            "denseRank": True,
                            "duplicateCount": True,
                            "rank": True,
                            "rowNumber": True,
                            "retrievedColumns": [],
                            "computedColumns": [
                                {
                                    "expr": "`学号`+$name",
                                    "name": "学号_2",
                                    "type": "string"
                                }
                            ]
                        }
                    },
                    "expressionsValue": "JSON",
                    "groupIndex": 0,
                    "groupName": "",
                    "id": "4pzAo3zNFF-gIrUQw9t1_07TdynDmipR5IxA",
                    "index": "1",
                    "runtime": "topn",
                    "stepName": "topn"
                }
            ],
            "notification": {
                "required": True
            },
            "oldImage": [
                {
                    "index": "1",
                    "ctype": "TopN",
                    "expressions": "{\"type\": \"topn\", \"code\": \"pyspark\", \"params\": {\"firstRows\": 1, \"lastRows\": 0, \"keys\": [], \"preFilter\": {\"distinct\": false, \"enabled\": false, \"expression\": \"\"}, \"orders\": [{\"column\": \"学号\", \"desc\": false}], \"denseRank\": false, \"duplicateCount\": false, \"rank\": false, \"rowNumber\": false, \"retrievedColumns\": [], \"computedColumns\": []}}",
                    "runtime": "topn",
                    "groupName": "",
                    "groupIndex": "0",
                    "pjName": "4pzAo3zNFF-gIrUQw9t1_Tutorial_Tutorial_developer_compute_tpn",
                    "id": "4pzAo3zNFF-gIrUQw9t1_07TdynDmipR5IxA",
                    "expressionsValue": "JSON",
                    "stepId": "1",
                    "stepName": "topn"
                }
            ],
            "ifsteps": 1
        }

        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()


