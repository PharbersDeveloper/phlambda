import json
import pytest
from phuserregister.src.main import lambdaHandler


class TestLmd:
    def test_fail_register(self):
        with open("../events/fail_register.json") as f:
            event = json.load(f)
        result = json.loads(lambdaHandler(event, " ")["body"])["data"]["message"]
        assert "this account alread register" == result

    def test_success_register(self):
        with open("../events/success_register.json") as f:
            event = json.load(f)
        result = json.loads(lambdaHandler(event, " ")["body"])["data"]["message"]
        assert "seccessfully register" == result


if __name__ == '__main__':
    pytest.main()
