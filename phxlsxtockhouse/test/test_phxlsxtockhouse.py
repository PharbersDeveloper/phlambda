import os
import pytest
import json
import src.main as main
import src.app as app


class TestLmd:
    def test_lmd(self):
        event = open("../events/event.json", "r").read()
        result = main.lambda_handler(json.loads(event), None)
        # result = app.lambda_handler(json.loads(event), None)
        print(result)
        # assert 'e' in a


if __name__ == '__main__':
    os.environ["PATH_PREFIX"] = "/Users/qianpeng/Desktop/"
    os.environ["BATCH_SIZE"] = "200"
    os.environ["CLICKHOUSE_HOST"] = "127.0.0.1"
    os.environ["CLICKHOUSE_PORT"] = "19000"
    os.environ["CLICKHOUSE_DB"] = "default"
    os.environ["REDIS_HOST"] = "127.0.0.1"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["LOCK_APP_NAME"] = "ds2clickhouse"
    os.environ["CHECK_APP_NAME"] = "rmds"
    # os.environ["AWS_ACCESS_KEY_ID"] = "ASIAWPBDTVEAPOQPBFWZ"
    # os.environ["AWS_SECRET_ACCESS_KEY"] = "x4o77Sj5voG+Zr8rPki6Y7feD2whXYHlt6sKkocX"
    # os.environ["AWS_SESSION_TOKEN"] = "IQoJb3JpZ2luX2VjED8aDmNuLW5vcnRod2VzdC0xIkgwRgIhAIIGIyeV/i2J3Kj3Fh+cv4n+3g6qyV+GtCtlv9bKoJtGAiEA/b5Rk57mI8JEIPUeP4wMp0bQuf1BxVRXPZjVmO1vc4oqlwIIbBACGgw0NDQ2MDM4MDM5MDQiDCCmKBHmgbl8oP5l6yr0AWA/aPFavkUxv0nVZJrOk/n/cmNm3X9jaH549tOoF+q060HlHwbSmlarXSrG/aT84nWl1eZbPCm5ow/geG9pi+fXbAksCDuAeAvILkeIX8wncix0jTXgf/yq7WntJMp+CqRRoNzirzgSfhkIewiem9EXte7pg8dXKqIpO8FYqrhCFe6k/5ojDe/eXMrBFBu8/WxVunxfZCEIFkC9NQj2ueRBU/z56myaSFRAgUMLMc19EGB2m5hf7aH5wHt+3ngUUgNbZbJd5W3gO65fkiNl5uagNjTFD3zt/8W9uBfYyV6LCtr34XD+MWYTbQAKigwQppFOyL8w4KqnkAY6nAH9ullGOIGzSIP/LzHa6uYBGVwqOdi6MkQLDVv8GV9WD7LNdTa9dgEK5CjSbJHOWjTa8Z9Wz8NTHmKBEUGxyhoDvGVvXbEyvVUzT83+HhT1RBenNUAaCZHjWiNb6e3Kqf5aEKAbW5qMjYT9ZbDv2aDlnOWXN+EQ69Omtr3b7BivsInyNYj75sKkHliYgJq6RRbLQFgbwG2Ah12eOW8="
    pytest.main()
