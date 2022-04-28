import os
import pytest
import json
import src.main as app


class TestLmd:
    def test_lmd(self):
        event = open("../events/event.json", "r").read()
        result = app.lambda_handler(json.loads(event), None)
        print(result)


if __name__ == '__main__':
    pytest.main()
