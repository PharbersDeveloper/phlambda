import os
import json
import pytest
import src.app as app


class TestGenLowCode:

    def test_gen_code(self):
        event = open("../events/event_gen_code.json", "r").read()
        event = {
            "Records": [
                {
                    "body": event
                }
            ]
        }
        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()
