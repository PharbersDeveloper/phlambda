
import pytest
import json
from src.main import lambda_handler


class TestLmd:

    def test_lmd_adapter_dict(self):
        with open('../event/event.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambda_handler(event, None)
            print(report)


if __name__ == '__main__':
    pytest.main()