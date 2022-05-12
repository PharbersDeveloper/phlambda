import os
import sys
import json
import pytest
import src.app as app
from handler.Command.RemoveS3Path import RemoveS3Path

# CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
# config_path = CURRENT_DIR.rsplit('/', 1)[0]  # 上级目录
# sys.path.append(config_path)

class TestSync:

    def test_rm_ds(self):
        with open("../events/event_remove_ds.json", "r", encoding="utf8") as fp:
            event = json.load(fp)
            app.lambda_handler(event, None)

    # def test_rm_job(self):
    #     with open("../events/event_remove_job.json", "r", encoding="utf8") as fp:
    #         event = json.load(fp)
    #         app.lambda_handler(event, None)

    def test_rm_s3(self):
        remove_s3_dir = f"""pharbers/HfSZTr74gRcQOYoA/A"""
        RemoveS3Path().execute({
            "bucket_name": "ph-platform",
            "s3_dir": f"""2020-11-11/lake/{remove_s3_dir}"""
        })


if __name__ == "__main__":
    os.environ["CLICKHOUSE_HOST"] = "127.0.0.1"
    os.environ["CLICKHOUSE_PORT"] = "19000"
    os.environ["CLICKHOUSE_DB"] = "default"
    os.environ["REDIS_HOST"] = "127.0.0.1"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["CHECK_APP_NAME"] = "ds2clickhouse"
    os.environ["LOCK_APP_NAME"] = "rmds"
    pytest.main()
