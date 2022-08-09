import json
import pytest
from phemail.src.main import lambdaHandler


class TestLmd:
    def test_send_email(self):
        with open("../event/event.json") as f:
            event = json.load(f)
        assert "seccessfully send emails" == json.loads(lambdaHandler(event, ' ')['body'])['data']['message']


if __name__ == '__main__':
    pytest.main()
