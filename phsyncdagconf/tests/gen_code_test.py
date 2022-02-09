import json
import pytest
import src.app as app


class TestGenCode:
    def test(self):
        event = open("../events/event_gen_code.json", "r").read()
        app.lambda_handler(json.loads(event), None)


if __name__ == '__main__':
    pytest.main()
