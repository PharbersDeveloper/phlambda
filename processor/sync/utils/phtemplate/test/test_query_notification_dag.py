import pytest
import json
import src.app as app


class TestQueryNotificationDag:

    def test_notification_dag(self):
        with open("../events/event_dag_notification.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            count = len(json.loads(result["body"]))
            print(json.loads(result["body"]))
            print(count)
            assert count > 0
            assert result["statusCode"] == 200

    def test_executionStatus_data(self):
        with open("../events/event_dag_execution.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            count = len(json.loads(result["body"]))
            print(json.loads(result["body"]))
            print(count)
            assert count > 0
            assert result["statusCode"] == 200


if __name__ == '__main__':
    pytest.main()
