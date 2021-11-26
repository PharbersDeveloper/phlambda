
import pytest
import json
from src.main import lambda_handler


class TestLmd:

    def test_lmd_adapter_dict(self):
        with open('../event/event_adapter_dict.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_lmd_adapter_error(self):
        with open('../event/event_adapter_error.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_lmd_adapter_list(self):
        with open('../event/event_adapter_list.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_lmd_default_default(self):
        with open('../event/event_default_default.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_lmd_default_max(self):
        with open('../event/event_default_max.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_lmd_default_None(self):
        with open('../event/event_default_None.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)

    def test_lmd_default_error(self):
        with open('../event/event_default_error.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)


if __name__ == '__main__':
    pytest.main()