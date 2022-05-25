import pytest
import src.main as app


class TestStop:
    def test_stop(self):
        event = {
            "body": {"runnerId": "automax_automax_developer_2022-05-25T05:07:37+00:00"}
        }
        app.lambda_handler(event, None)


if __name__ == "__main__":

    pytest.main()
