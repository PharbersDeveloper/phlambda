import json

import pytest
from src.main import lambda_handler


class TestLmd:

    def test_lmd(self):
        with open("../events/event.json", 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            lambda_handler(event, None)


if __name__ == '__main__':
    TestLmd().test_lmd()
