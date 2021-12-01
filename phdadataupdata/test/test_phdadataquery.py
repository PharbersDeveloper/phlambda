
import pytest
import json
from src.main import lambdaHandler


class TestLmd:

    def test_lmd_adapter_dict(self):
        with open('../event/event.json', 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            report = lambdaHandler(event, None)
            print(report)


if __name__ == '__main__':
    pytest.main()