import pytest
import json
import src.app as app


class TestQueryDynamoDB:
    def test_get_deletion_impact(self):
        with open("../events/event_compute_deletion_impact.json", "r", encoding="utf8") as file:
            event = json.load(file)
            result = app.lambda_handler(event, None)
            print(result)
            assert result["statusCode"] == 200


if __name__ == '__main__':
    pytest.main()
