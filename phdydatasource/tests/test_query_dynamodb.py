import pytest
import json
from src.util.Convert2JsonAPI import Convert2JsonAPI
from src.models.Execution import Execution


class TestQueryDynamoDB:

    def test_query(self):
        data = [
            Execution({"id": "1", "state": "state", "input": "input",
                       "owner": "owner", "startTime": 111, "endTime": 333, "steps": "[]"}),
            Execution({"id": "2", "state": "state", "input": "input",
                       "owner": "owner", "startTime": 222, "endTime": 444, "steps": "[]"})]

        result = json.loads(Convert2JsonAPI(Execution).mc(many=True).dumps(data))
        assert "data" in list(result.keys())
