import pytest
import json
from phlambda.phforwarddyevent.src.main import lambda_handler

class TestLmd:

    def test_lmd_clear_DS_data(self):
        with open("../events/event_clear_DS_data.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')

    def test_lmd_dag_create(self):
        with open("../events/event_dag_create.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')

    def test_lmd_dag_refresh(self):
        with open("../events/event_dag_refresh.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')

    def test_lmd_edit_sample(self):
        with open("../events/event_edit_sample.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')


    def test_lmd_prepare_edit(self):
        with open("../events/event_prepare_edit.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')


    def test_lmd_project_file_to_DS(self):
        with open("../events/event_project_file_to_DS.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')

    def test_lmd_remove_DS(self):
        with open("../events/event_remove_DS.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')

    def test_lmd_remove_Job(self):
        with open("../events/event_remove_Job.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')


    def test_lmd_resource_create(self):
        with open("../events/event_resource_create.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')

    def test_lmd_resource_delete(self):
        with open("../events/event_resource_delete.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')

    def test_lmd_transform_schema(self):
        with open("../events/event_transform_schema.json") as f:
            event = json.load(f)
        assert "success" == lambda_handler(event, '')



if __name__ == '__main__':
    pytest.main()
