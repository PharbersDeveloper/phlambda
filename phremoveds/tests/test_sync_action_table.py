import pytest
import json
import src.app as app


class TestSync:

    # def test_rm_ds(self):
    #     with open("../events/event_remove_ds.json", "r", encoding="utf8") as fp:
    #         event = json.load(fp)
    #         app.lambda_handler(event, None)

    def test_rm_job(self):
        with open("../events/event_remove_job.json", "r", encoding="utf8") as fp:
            event = json.load(fp)
            app.lambda_handler(event, None)


if __name__ == "__main__":
    pytest.main()
