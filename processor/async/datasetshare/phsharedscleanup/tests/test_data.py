import pytest
import src.main as app


class TestDSCleanUp:
    def test_clean_up(self):
        event = {
            "projectId": "RL8iefdfGuRfbuN",
            "owner": "xx",
            "showName": "xx",
            "tenantId": "",
            "shares": [
                {
                    "target": "A",
                    "targetCat": "catalog",
                    "targetPartitionKeys": [
                        {
                            "name": "key1",
                            "type": "string"
                        },
                        {
                            "name": "key2",
                            "type": "string"
                        }
                    ],
                    "sourceSelectVersions": [
                        "1"
                    ],
                    "source": "B"
                }
            ],
            "error": {
                "Error": "",
                "Cause": ""
            }
        }
        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()
