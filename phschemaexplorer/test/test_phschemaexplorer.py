import pytest
import os
import json
import src.main as app


class TestLmd:
    def test_lmd(self):
        os.environ["PATH_PREFIX"] = "../events/{project}/"
        event = open("../events/event_find.json", "r").read()
        result = app.lambda_handler(json.loads(event), None)
        assert len(result) == 1
        assert "readNumber" in result[0]
        assert "sheet" in result[0]
        assert "schema" in result[0]
        assert "data" in result[0]


if __name__ == '__main__':
    pytest.main()
