import os
import pytest
import json
import src.app as app


class TestLmd:
    def test_lmd(self):
        os.environ["PATH_PREFIX"] = "/Users/qianpeng/Desktop/"
        os.environ["BATCH_SIZE"] = "100"
        os.environ["CLICKHOUSE_HOST"] = "localhost"
        os.environ["CLICKHOUSE_PORT"] = "19000"
        os.environ["CLICKHOUSE_DB"] = "default"
        event = open("../events/event.json", "r").read()
        result = app.lambda_handler(json.loads(event), None)
        print(result)
        # assert 'e' in a


if __name__ == '__main__':
    pytest.main()
