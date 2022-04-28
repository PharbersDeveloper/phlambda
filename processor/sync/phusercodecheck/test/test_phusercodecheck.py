import json

import pytest
from phusercodecheck.src.main import lambdaHandler


class TestLmd:
    def test_False(self):
        with open("../events/test_False.json", "r") as f:
            event = json.load(f)
        result = json.loads(lambdaHandler(event, " ")["body"])["message"]
        assert 'Code false' == result
    def test_True(self):
        with open("../events/test_True.json", "r") as f:
            event = json.load(f)
        result = json.loads(lambdaHandler(event, " ")["body"])["message"]
        assert 'Code correct' == result

if __name__ == '__main__':
    pytest.main()
