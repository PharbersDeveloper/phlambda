import pytest
import main as app


class TestDeletion:

    def test_deletion_step(self):
        event = {
            "scripts": [
                {
                    "projectId": "RL8iefdfGuRfbuN",
                    "operatorParameters": "",
                    "actionName": "compute_C",
                    "outputs": "C",
                    "runtime": "topn",
                    "showName": "鹏钱",
                    "jobDisplayName": "Alex_Alex_developer_compute_C",
                    "jobVersion": "developer",
                    "prop": "",
                    "jobId": "MWJTtgs2VBrMzMi",
                    "projectName": "Alex",
                    "jobPath": "2020-11-11/jobs/python/phcli/Alex_Alex_developer/Alex_Alex_developer_compute_C/phjob.py",
                    "jobName": "developer_MWJTtgs2VBrMzMi_Alex_Alex_compute_C",
                    "timeout": 1000,
                    "dagName": "Alex",
                    "labels": "",
                    "jobShowName": "compute_C",
                    "owner": "5UBSLZvV0w9zh7-lZQap",
                    "flowVersion": "developer",
                    "id": "MWJTtgs2VBrMzMi",
                    "traceId": "7890ec3821a949a78ea67f93f6c9497c",
                    "inputs": "[\"A\"]"
                },
                {
                    "projectId": "RL8iefdfGuRfbuN",
                    "operatorParameters": "",
                    "actionName": "compute_C",
                    "outputs": "C",
                    "runtime": "group",
                    "showName": "鹏钱",
                    "jobDisplayName": "Alex_Alex_developer_compute_C",
                    "jobVersion": "developer",
                    "prop": "",
                    "jobId": "MWJTtgs2VBrMzMi",
                    "projectName": "Alex",
                    "jobPath": "2020-11-11/jobs/python/phcli/Alex_Alex_developer/Alex_Alex_developer_compute_C/phjob.py",
                    "jobName": "developer_MWJTtgs2VBrMzMi_Alex_Alex_compute_C",
                    "timeout": 1000,
                    "dagName": "Alex",
                    "labels": "",
                    "jobShowName": "compute_C",
                    "owner": "5UBSLZvV0w9zh7-lZQap",
                    "flowVersion": "developer",
                    "id": "MWJTtgs2VBrMzMi",
                    "traceId": "7890ec3821a949a78ea67f93f6c9497c",
                    "inputs": "[\"A\"]"
                },
                {
                    "projectId": "RL8iefdfGuRfbuN",
                    "operatorParameters": "",
                    "actionName": "compute_C",
                    "outputs": "C",
                    "runtime": "pyspark",
                    "showName": "鹏钱",
                    "jobDisplayName": "Alex_Alex_developer_compute_C",
                    "jobVersion": "developer",
                    "prop": "",
                    "jobId": "MWJTtgs2VBrMzMi",
                    "projectName": "Alex",
                    "jobPath": "2020-11-11/jobs/python/phcli/Alex_Alex_developer/Alex_Alex_developer_compute_C/phjob.py",
                    "jobName": "developer_MWJTtgs2VBrMzMi_Alex_Alex_compute_C",
                    "timeout": 1000,
                    "dagName": "Alex",
                    "labels": "",
                    "jobShowName": "compute_C",
                    "owner": "5UBSLZvV0w9zh7-lZQap",
                    "flowVersion": "developer",
                    "id": "MWJTtgs2VBrMzMi",
                    "traceId": "7890ec3821a949a78ea67f93f6c9497c",
                    "inputs": "[\"A\"]"
                }
            ]
        }
        app.lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main()
