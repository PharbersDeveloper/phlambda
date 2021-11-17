import json
import pytest
from phresetpwd.src.main import lambdaHandler


class TestLmd:

    def test_pwd_email(self):
        with open("../event/event.json") as f:
            event = json.load(f)
        assert "successfully send emails" == json.loads(lambdaHandler(event, ' ')['body'])['data']['message']


if __name__ == '__main__':
    pytest.main()
