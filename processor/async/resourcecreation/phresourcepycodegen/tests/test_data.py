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
            "owner": "001-02-04-8",
            "showName": "Alex",
            "script": {
                "name": "compute_topn",
                "flowVersion": "developer",
                "runtime": "topn",
                "inputs": "[\"Alex\", \"Alex2\"]",
                "output": "topn_output"
            }
        }
        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()


