import json
import pytest
import src.main as app


class TestGenerateCode:
    def test_generate(self):
        event = {
            "traceId": "50cc15f3b88f40c7bd43d2d10badc214",
            "tenantId": "zudIcG_17yj8CEUoCTHg",
            "projectId": "RL8iefdfGuRfbuN",
            "projectName": "Alex",
            "flowVersion": "developer",
            "dagName": "Alex",
            "owner": "5UBSLZvV0w9zh7-lZQap",
            "showName": "鹏钱",
            "script": {
                "name": "compute_PySparkD",
                "flowVersion": "developer",
                "runtime": "pyspark",
                "inputs": "[\"PythonC\"]",
                "output": "PySparkD"
            }
        }
        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()


