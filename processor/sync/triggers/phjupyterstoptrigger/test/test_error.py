import json

import pytest
from src.main import lambda_handler

event = {"body": json.dumps({
    "tenantId": "zudIcG_17yj8CEUoCTHg",
    "traceId": "alfred-resource-creation-traceId",
    "owner": "alfred",
    "showName": "alfred"
})}


class TestLmd:
    def test_lmd(self):
        report = lambda_handler(event, None)
        print(report)


if __name__ == '__main__':
    TestLmd().test_lmd()
