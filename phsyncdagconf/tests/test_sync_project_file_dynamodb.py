import pytest
import json
from phlambda.phsyncdagconf.src.delegate.SyncDagConfToDynamoDB import SyncDagConfToDynamoDB


class TestSync:

    def test_sync(self):
        with open("../events/event.json") as f:
            event = json.load(f)
            app = SyncDagConfToDynamoDB(event=event)
            app.exec()


if __name__ == "__main__":
    sc = TestSync()
    sc.test_sync()
