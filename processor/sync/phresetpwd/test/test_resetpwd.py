import json
import pytest
from phresetpwd.src.main import lambdaHandler


class TestLmd:
    def testTrue(self):
        with open("../events/testTrue.json") as f:
            event = json.load(f)
        result = lambdaHandler(event, ' ')
        assert 'change password success' == json.loads(result['body'])['data']['message']
    def testFalse(self):
        with open("../events/testFalse.json") as f:
            event = json.load(f)
        result = lambdaHandler(event, ' ')
        assert 'change password failure' == json.loads(result['body'])['data']['message']

if __name__ == '__main__':
    pytest.main()
