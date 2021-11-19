import pytest
import json
from src.util.Convert2JsonAPI import Convert2JsonAPI
from src.models.Execution import Execution
from src.models.Partition import Partition
import src.app as app


class TestQueryDynamoDB:

    def test_dataset_query(self):
        with open("../events/event_query.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            print(result)
            assert result["statusCode"] == 200

    def test_dataset_scan(self):
        with open("../events/event_scan.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            print(result)
            assert result["statusCode"] == 200

    def test_dataset_put(self):
        with open("../events/event_put.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            print(result)
            assert result["statusCode"] == 200

    def test_dataset_delete(self):
        with open("../events/event_delete.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            print(result)
            assert result["statusCode"] == 200

    def test_notification_batch_item(self):
        with open("../events/event_batch.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            print(result)
            assert result["statusCode"] == 200

    # def test_execution_query(self):
    #     data = [
    #         Execution({"id": "1", "state": "state", "input": "input",
    #                    "owner": "owner", "startTime": 111, "endTime": 333, "steps": "[]"}),
    #         Execution({"id": "2", "state": "state", "input": "input",
    #                    "owner": "owner", "startTime": 222, "endTime": 444, "steps": "[]"})]
    #
    #     result = json.loads(Convert2JsonAPI(Execution, many=False).build().dumps(data))
    #     assert "data" in list(result.keys())
    #
    # def test_partition_query(self):
    #     data = [
    #         Partition({
    #             "id": "aaa",
    #             "smID": "bbb",
    #             "source": "aa/aaa/aa",
    #             "schema": """{"name": "alex"}""",
    #             "date": 11111111111,
    #             "partitions": [{"a": 1}, {"b": 2}]
    #         })
    #     ]
    #     result = json.loads(Convert2JsonAPI(Partition, many=True).build().dumps(data))
    #     assert "data" in list(result.keys())


if __name__ == '__main__':
    pytest.main()
