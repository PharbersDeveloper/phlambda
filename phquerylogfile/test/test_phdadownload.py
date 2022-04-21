import pytest
import json
from src.main import lambda_handler


class TestLmd:
    def test_lmd(self):
        with open('../event/event.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_notItem(self):
        with open('../event/event_not_Item.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_not_Logs(self):
        with open('../event/event_not_logs.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_output(self):
        with open('../event/event_output.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)


if __name__ == '__main__':
    TestLmd().test_lmd()
