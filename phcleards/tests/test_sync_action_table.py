import os
import pytest
import json
import src.app as app


class TestSync:

    def test_sync(self):
        with open("../events/event_clear.json", "r", encoding="utf8") as fp:
            event = json.load(fp)
            app.lambda_handler(event, None)


if __name__ == "__main__":
    os.environ["CLICKHOUSE_HOST"] = "127.0.0.1"
    os.environ["CLICKHOUSE_PORT"] = "19000"
    os.environ["CLICKHOUSE_DB"] = "default"
    os.environ["REDIS_HOST"] = "127.0.0.1"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["CHECK_APP_NAME"] = "ds2clickhouse"
    os.environ["LOCK_APP_NAME"] = "rmds"
    pytest.main()
