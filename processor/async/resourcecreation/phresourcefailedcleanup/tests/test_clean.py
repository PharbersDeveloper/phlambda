
import pytest
from src.main import lambda_handler


event = {
    "traceId": "17f18b6b6d2e4b0fbec17f0a3a07e669",
    "projectId": "ggjpDje0HUC2JW",
    "owner": "cleanuptesttraceidowner",
    "showName": "cleanuptestshownamec",
    "datasets": [
        {
            "id": "123abctest",
            "name": "123abctest",
            "cat": "intermediate",
            "format": "parquet"
        }
    ],
    "scripts": {
        "id": "1234abctest1",
        "jobName": "1234abctest1",
        "actionName": "1234abctest1",
        "flowVersion": "1234abctest1",
        "inputs": "[]",
        "output": "{}"
    },
    "errors": {
        "Error": "Exception",
        "Cause": ""
    }
}

# 1. common 必须存在
# 2. action 必须存在
# 3. notification 必须存在
# 4. datasets 和 scripts 必须存在一个
#   4.1 如果dataset存在，name, cat, format 都必须存在，并判断类型
#   4.2 如果scripts存在，name, flowVersion, input, output 都必须存在，并判断类型


class TestLmd:
    def test_lmd(self):
        report = lambda_handler(event, None)
        print(report)


if __name__ == '__main__':
    TestLmd().test_lmd()
