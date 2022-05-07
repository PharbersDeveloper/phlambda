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
            "traceId": "alfred-resource-creation-traceId",
            "dagName": "demo",
            "owner": "alex_qian_00001",
            "showName": "钱鹏",
            "projectName": "demo",
            "projectId": "ggjpDje0HUC2JW",
            "script": {
                "name": "compute_BB",
                "flowVersion": "developer",
                "runtime": "r",
                "inputs": "[\"AA\"]",
                "output": "BB",
                "id": "001"
            }
        }
        app.lambda_handler(event, None)


if __name__ == "__main__":

    pytest.main()
