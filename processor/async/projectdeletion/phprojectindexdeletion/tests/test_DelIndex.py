import pytest
from main import lambda_handler

event = {
    "common": {
        "traceId": "1ecf64ce0a7441cc9db9f118f93gb423",
        "tenantId": "zudIcG_17yj8CEUoCTHg",
        "projectId": "1qxPsO7lzQAU6Yx",
        "projectName": "ABC",
        "owner": "alfred",
        "showName": "alfred"
    },
    "action": {
        "cat": "tenantStop",
        "desc": "terminate project",
        "comments": "something need to say",
        "message": "something need to say",
        "required": True
    },
    "resources": [
        "emr", "clickhouse", "chproxy"
    ],
    "notification": {
        "required": True
    }
}

class TestLmd:
    def test_lmd(self):
        report = lambda_handler(event['common'], None)

        assert "ok" == report['status']

if __name__ == '__main__':
    pytest.main()

