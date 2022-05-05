# dag
#
# projectId   -->   projectId
# representId -->   job(job_Id) ds(dsI)  link(link_id)
# cat         -->   ds job
# cmessage    -->   node(job_message) link(sourceId,targerId)
# ctype       -->   node link
# name        -->   job dag_name + flow_version + job_name + job_version
#                   ds ds_name
#                   link None
# position    -->   x,y,z
# level       -->   1,2,3,4,5
#
# dagconf
# dag_name      -->  dag_name
# flow_version  -->  branch_name
# job_name      -->  file_name
# job_id        -->  job_id
# inputs        -->  inputs(dsID, dsName)
# outputs       -->  outputs
# job_version   -->  job_version
# projectId     -->  projectId
# timeout       -->  timeout
# runtime       -->  python3,R,pyspark,sparkR
#

import os
import pytest
import src.main as app


class TestCreateRFile:
    def test_create(self):
        event = {
            "traceId": "001",
            "projectId": "project_id_001",
            "owner": "alex_001",
            "showName": "Alex",
            "projectName": "Alex_Test",
            "dagName": "Dag_Name",
            "jobDisplayName": "A_C_B",
            "scripts": {
                "id": "id_001",
                "jobName": "001s_A_C_B",
                "actionName": "action_name",
                "flowVersion": "developer",
                "inputs": "[{\"name\": \"A\"}, {\"name\": \"B\"}, {\"name\": \"C\"}]",
                "output": "{\"name\": \"D\"}"
            }
        }
        app.lambda_handler(event, None)


if __name__ == "__main__":
    os.environ["BUCKET"] = "ph-platform"
    os.environ["CLI_VERSION"] = "2020-11-11"
    # os.environ["JOB_PATH_PREFIX"] = "/tmp/phjobs/"
    os.environ["JOB_PATH_PREFIX"] = "/Users/qianpeng/Desktop/TestCreateFIle/"
    os.environ["TM_PHMAIN_FILE"] = "/template/python/phcli/maxauto/phmain-r_dev.tmp"
    os.environ["TM_PHJOB_FILE"] = "/template/python/phcli/maxauto/phjob-r_dev.tmp"
    os.environ["DAG_S3_JOBS_PATH"] = "/jobs/python/phcli/"
    pytest.main()
