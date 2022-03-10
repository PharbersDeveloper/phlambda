import pytest
import json
import src.main as main


class TestLmd:
    def test_lmd(self):
        with open("../events/event.json", "r", encoding="utf8") as f:
            event = json.load(f)
            main.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()
