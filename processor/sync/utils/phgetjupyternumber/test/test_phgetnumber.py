import pytest
import json
from src.main import lambda_handler


class TestLmd:
    def test_lmd_success(self):
        with open("../events/test_lmd_success.json") as f:
            event = json.load(f)
        result = lambda_handler(event, " ")
        print(result)


if __name__ == "__main__":
    pytest.main()
