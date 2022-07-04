import json
import os
import pytest
import src.main as app


class TestCreateRFile:
    def test_create(self):
        with open("../events/event-start.json", 'r', encoding='utf8') as fp:
            event = (json.loads(fp.read()))
            app.lambda_handler(event, None)


if __name__ == "__main__":

    pytest.main()
