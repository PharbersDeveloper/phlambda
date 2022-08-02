import json
from datetime import datetime
#import boto3
#from boto3.dynamodb.conditions import Key
from puttonotification import put_notification
#from pherrorlayer import *
import re
#-- 本地测试用 --#
from error import *



def ChangeStrToDict(data):
    return json.loads(data) if isinstance(data, str) else data

def FindErrorKey(key):
    Patter = re.compile(pattern='error',flags=re.IGNORECASE)
    result = Patter.findall(string=key)
    return True if len(result) > 0 else False

def FindErrorCause(data):
    data = ChangeStrToDict(data)
    try:
        tag = ChangeStrToDict(data['Cause'])
        return tag
    except:
        return False

def SearchErrorType(error):
    keys = ChangeStrToDict(error).keys()
    keys = list(filter(lambda x: FindErrorKey(x) is True, keys))
    if len(keys) == 0:
        return None
    else:
        cause = list(filter(lambda x: FindErrorCause(error[x]) is not False, keys))
        cause = list(map(lambda x: FindErrorCause(error[x]), cause))
        if len(cause) == 0:
            return None
        return cause

def MapErrorType(cause):

    if cause is None:
        print("未知错误")
        #Errors()  默认错误
    else:
        #--- 错误详情，用于解析映射用 -----#
        ErrorKeys = list(*map(lambda x: list(x.keys()), cause))
        print(ErrorKeys)
        if "ExecutionArn" in ErrorKeys:
            print("EMR 错误")

#---- 处理抛出的错误信息 -----------#
def lambda_handler(event, context):
    print("*"*50 + " EVENT " + "*"*50)
    print(event)

    error = event["error"]
    print("*"*50 + " ERROR " + "*"*50)
    print(error)

    cause = SearchErrorType(error)
    print(cause)

    MapErrorType(cause)

    #TODO 目前对事件错误信息掌握不全，需要多次测试后再编写映射逻辑
    #---- 基于error信息映射pherrorlayer ----------#


    #dt = datetime.now()
    #ts = datetime.timestamp(dt)
    #put_notification(event['runnerId'], pid, None, 0, "", int(ts), event['owner'], event['showName'], status='running')

    return {}
if __name__ == '__main__':
    #a = "executeError"

    event = {
        "owner":"35cca7e1-45d9-4a6e-80f6-09e5417feb33",
        "Input":{
            "common":{
                "runnerId":"sample_sample_developer_2022-08-02T06:20:10+00:00",
                "projectId":"4pzAo3zNFFewrwe-gIrUQw9t1",
                "projectName":"sample",
                "owner":"35cca7e1-45d9-4a6e-80f6-09e5417feb33",
                "showName":"\u6717\u8f69\u9f50"
            },
            "compute_sample":{
                "name":"compute_sample",
                "type":"spark-submit",
                "clusterId":"j-3VPMNC2QH7UBC",
                "HadoopJarStep":{
                    "Jar":"command-runner.jar",
                    "Args":[
                        "spark-submit",
                        "--deploy-mode",
                        "cluster",
                        "--conf",
                        "spark.driver.cores=1",
                        "--conf",
                        "spark.driver.memory=1g",
                        "--conf",
                        "spark.executor.cores=1",
                        "--conf",
                        "spark.executor.memory=1g",
                        "--conf",
                        "spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
                        "--conf",
                        "spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8",
                        "--jars",
                        "s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/clickhouse-jdbc-0.2.4.jar,s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/guava-30.1.1-jre.jar",
                        "--py-files",
                        "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-4.0.0-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/sample_sample_developer/sample_sample_developer_compute_sample/phjob.py",
                        "s3://ph-platform/2020-11-11/jobs/python/phcli/sample_sample_developer/sample_sample_developer_compute_sample/phmain.py",
                        "--owner",
                        "dev\u73af\u5883",
                        "--dag_name",
                        "sample_sample_developer",
                        "--run_id",
                        "sample_sample_developer_2022-08-02T06:20:10+00:00",
                        "--job_full_name",
                        "sample_sample_developer_compute_sample",
                        "--tenant_ip",
                        "192.168.32.26",
                        "--ph_conf",
                        "{\"projectName\": \"sample\", \"showName\": \"\u6717\u8f69\u9f50\", \"sourceProjectId\": \"4pzAo3zNFFqreq-gIrUQw9t1\", \"targetProjectId\": \"4pzAo3zNFF-geqrewIrUQw9t1\", \"datasetId\": \"olMNMgPVLlbvwrewqr8Y6\", \"datasetType\": \"uploaded\", \"datasetName\": \"Groupwrewq\", \"sample\": \"F_1\", \"company\": \"pharbers\"}"
                    ]
                }
            }
        },
        "showName":"\u6717\u8f69\u9f50",
        "engine":{
            "type":"awsemr",
            "id":"j-3VPMNC2QH7UBC",
            "dss":{
                "ip":"192.168.32.26"
            }
        },
        "runnerId":"sample_sample_developer_2022-08-02T06:20:10+00:00",
        "projectName":"sample",
        "error":{
            "executeError":{
                "Error":"States.TaskFailed",
                "Cause":"{\"ExecutionArn\":\"arn:aws-cn:states:cn-northwest-1:444603803904:execution:sample-sample-developer-2022-08-02T06-20-10-00-00:56fae7d2-f366-4dce-8773-b3c120e74c6e\",\"Input\":\"{\\\"common\\\":{\\\"runnerId\\\":\\\"sample_sample_developer_2022-08-02T06:20:10+00:00\\\",\\\"projectId\\\":\\\"4pzAo3zNFFewrwe-gIrUQw9t1\\\",\\\"projectName\\\":\\\"sample\\\",\\\"owner\\\":\\\"35cca7e1-45d9-4a6e-80f6-09e5417feb33\\\",\\\"showName\\\":\\\"\u6717\u8f69\u9f50\\\"},\\\"compute_sample\\\":{\\\"name\\\":\\\"compute_sample\\\",\\\"type\\\":\\\"spark-submit\\\",\\\"clusterId\\\":\\\"j-3VPMNC2QH7UBC\\\",\\\"HadoopJarStep\\\":{\\\"Jar\\\":\\\"command-runner.jar\\\",\\\"Args\\\":[\\\"spark-submit\\\",\\\"--deploy-mode\\\",\\\"cluster\\\",\\\"--conf\\\",\\\"spark.driver.cores=1\\\",\\\"--conf\\\",\\\"spark.driver.memory=1g\\\",\\\"--conf\\\",\\\"spark.executor.cores=1\\\",\\\"--conf\\\",\\\"spark.executor.memory=1g\\\",\\\"--conf\\\",\\\"spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8\\\",\\\"--conf\\\",\\\"spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8\\\",\\\"--jars\\\",\\\"s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/clickhouse-jdbc-0.2.4.jar,s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/guava-30.1.1-jre.jar\\\",\\\"--py-files\\\",\\\"s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-4.0.0-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/sample_sample_developer/sample_sample_developer_compute_sample/phjob.py\\\",\\\"s3://ph-platform/2020-11-11/jobs/python/phcli/sample_sample_developer/sample_sample_developer_compute_sample/phmain.py\\\",\\\"--owner\\\",\\\"dev\u73af\u5883\\\",\\\"--dag_name\\\",\\\"sample_sample_developer\\\",\\\"--run_id\\\",\\\"sample_sample_developer_2022-08-02T06:20:10+00:00\\\",\\\"--job_full_name\\\",\\\"sample_sample_developer_compute_sample\\\",\\\"--tenant_ip\\\",\\\"192.168.32.26\\\",\\\"--ph_conf\\\",\\\"{\\\\\\\"projectName\\\\\\\": \\\\\\\"sample\\\\\\\", \\\\\\\"showName\\\\\\\": \\\\\\\"\u6717\u8f69\u9f50\\\\\\\", \\\\\\\"sourceProjectId\\\\\\\": \\\\\\\"4pzAo3zNFFqreq-gIrUQw9t1\\\\\\\", \\\\\\\"targetProjectId\\\\\\\": \\\\\\\"4pzAo3zNFF-geqrewIrUQw9t1\\\\\\\", \\\\\\\"datasetId\\\\\\\": \\\\\\\"olMNMgPVLlbvwrewqr8Y6\\\\\\\", \\\\\\\"datasetType\\\\\\\": \\\\\\\"uploaded\\\\\\\", \\\\\\\"datasetName\\\\\\\": \\\\\\\"Groupwrewq\\\\\\\", \\\\\\\"sample\\\\\\\": \\\\\\\"F_1\\\\\\\", \\\\\\\"company\\\\\\\": \\\\\\\"pharbers\\\\\\\"}\\\"]}}}\",\"InputDetails\":{\"Included\":true},\"Name\":\"56fae7d2-f366-4dce-8773-b3c120e74c6e\",\"StartDate\":1659425992717,\"StateMachineArn\":\"arn:aws-cn:states:cn-northwest-1:444603803904:stateMachine:sample-sample-developer-2022-08-02T06-20-10-00-00\",\"Status\":\"FAILED\",\"StopDate\":1659426049310}"
            }
        },
        "projectId":"4pzAo3zNFFewrwe-gIrUQw9t1"
    }

    lambda_handler(event,"")



