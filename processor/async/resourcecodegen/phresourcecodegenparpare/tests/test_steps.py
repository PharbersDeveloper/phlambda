import pytest
import main


class TestSteps:

    def test_steps(self):
        conf = {
            "traceId": "alfred-resource-creation-traceId",
            "projectId": "alextest",
            "projectName": "demo",
            "flowVersion": "developer",
            "dagName": "demo",
            "owner": "hbzhao",
            "showName": "赵浩博",
            "script": {
                "id": "",
                "jobName": "compute_十多个",
                "jobPath": "",
                "inputs": ["AA"],
                "outputs": [],
                "runtime": "prepare"
            },
            "steps": [
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
                            "value": "5"
                        }
                    }
                },
            ]
        }
        result = main.lambda_handler(conf, None)
        print(result)


if __name__ == '__main__':
    pytest.main()
