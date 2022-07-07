from datetime import datetime
from PutNotification import put_notification
from CreateArgsOfExecution import create_args_of_execution
import os



def  get_timestamp_of_localtime():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    return ts


def lambda_handler(event, context):
    # cicd 1317
    print(event)

    #----------------- args --------------------------------#
    runnerId, projectId, owner, showName = event['runnerId'], event['projectId'], event['owner'], event['showName']
   #----------------- args --------------------------------#


    #----------------- put notification --------------------#
    ts = get_timestamp_of_localtime()
    put_notification(runnerId, projectId, None, 0, "", int(ts), owner, showName)
    #----------------- put notification --------------------#


    #---------------- create args of execution -------------#
    sm_of_share = "s3://ph-platform/2020-11-11/jobs/python/phcli/shareDataSet_dev/share/sm_of_share.json"
    execute_py, phmain_py = "s3://ph-platform/2020-11-11/jobs/python/phcli/shareDataSet_dev/share/phjob.py",\
                            "s3://ph-platform/2020-11-11/jobs/python/phcli/shareDataSet_dev/share/phmain.py"

    args_of_execution = create_args_of_execution(execute_py, phmain_py, os.getenv("shareProject"), event)
    #---------------- create args of execution -------------#



    return {
        "args": args_of_execution,
        "sm": sm_of_share
    }
