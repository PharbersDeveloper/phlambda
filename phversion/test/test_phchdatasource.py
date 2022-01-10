import pytest
import json
from src import main


class TestSync:

    def test_sync(self):
        with open("../events/event.json", "r", encoding="utf8") as fp:
            event = json.load(fp)
            print(main.lambda_handler(event, None))


if __name__ == "__main__":
    sc = TestSync()
    sc.test_sync()
