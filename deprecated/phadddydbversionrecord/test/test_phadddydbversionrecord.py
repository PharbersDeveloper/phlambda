import pytest
import json
import sys
import os
CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
config_path = CURRENT_DIR.rsplit('/', 1)[0]  # 上级目录
sys.path.append(config_path)
from src import main


class TestLmd:
    def test_lmd_trigger(self):
        with open('../event/events.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = main.lambda_handler(event, None)
            print(report)


if __name__ == '__main__':
    pytest.main()