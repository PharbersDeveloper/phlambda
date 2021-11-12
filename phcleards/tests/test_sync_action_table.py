import pytest
import json
import src.app as app


class TestSync:

    def test_sync(self):
        with open("../events/event_clear.json", "r", encoding="utf8") as fp:
            event = json.load(fp)
            app.lambda_handler(event, None)


if __name__ == "__main__":
    pytest.main()
