import pytest
import json
import src.main as app


class TestLmd:
    def test_lmd(self):
        with open("../event/event.json", "r", encoding="utf8") as fp:
            event = json.load(fp)
            app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()
