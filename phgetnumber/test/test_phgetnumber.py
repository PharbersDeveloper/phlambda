import pytest
import json
from phgetnumber.src.main import lambda_handler


class TestLmd:
    def test_lmd_success(self):
        with open("../events/test_lmd_success.json") as f:
            event = json.load(f)
        result = lambda_handler(event, " ")
        result = json.loads(result["body"])
        assert result["message"] == 7

    def test_lmd_false(self):
        with open("../events/test_lmd_false.json") as f:
            event = json.load(f)
        result = lambda_handler(event, " ")
        result = json.loads(result["body"])
        assert result["message"] == 0


if __name__ == "__main__":
    pytest.main()
