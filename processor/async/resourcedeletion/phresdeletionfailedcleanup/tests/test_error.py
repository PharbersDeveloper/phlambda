
import json
import pytest
from src.main import lambda_handler


class TestLmd:
    def test_lmd(self):
        with open('args.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            print(event)
            report = lambda_handler(event, None)
            print(report)


if __name__ == '__main__':
    TestLmd().test_lmd()
