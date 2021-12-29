import pytest
import json
import src.app as app


class TestQueryDynamoDB:
    # def test_put(self):
    #     with open("../events/event_put.json", "r", encoding="utf8") as file:
    #         event = json.load(file)
    #         result = app.lambda_handler(event, None)
    #         print(result)
    #         assert result["statusCode"] == 200

    # def test_query(self):
    #     with open("../events/event_query.json", "r", encoding="utf8") as file:
    #         event = json.load(file)
    #         result = app.lambda_handler(event, None)
    #         count = len(json.loads(result["body"])["data"])
    #         print(count)
    #         assert count > 0
    #         assert result["statusCode"] == 200
    #
    # def test_scan(self):
    #     with open("../events/event_scan.json", "r", encoding="utf8") as file:
    #         event = json.load(file)
    #         result = app.lambda_handler(event, None)
    #         count = len(json.loads(result["body"])["data"])
    #         print(count)
    #         assert count > 0
    #         assert result["statusCode"] == 200
    #
    # def test_batch_item(self):
    #     with open("../events/event_batch.json", "r", encoding="utf8") as file:
    #         event = json.load(file)
    #         result = app.lambda_handler(event, None)
    #         count = len(json.loads(result["body"])["data"])
    #         print(count)
    #         assert count > 0
    #         assert result["statusCode"] == 200

    def test_begins_with_item(self):
        with open("../events/event_query_begins_with.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            count = len(json.loads(result["body"])["data"])
            print(count)
            assert count > 0
            assert result["statusCode"] == 200

    # def test_delete(self):
    #     with open("../events/event_delete.json", "r", encoding="utf8") as file:
    #         event = json.load(file)
    #         result = app.lambda_handler(event, None)
    #         print(result)
    #         assert result["statusCode"] == 200


if __name__ == '__main__':
    pytest.main()
