import boto3
import json

'''
args = {
        "runnerId.$": "$.common.runnerId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "engine.$": "$.engine",
        "calculate.$": "$.calculate",
        "tenantId.$": "$.common.tenantId"
      }
'''



dynamodb = boto3.resource('dynamodb')

def put_notification(runnerId, projectId, category, code, comments, date, owner, showName,
                     jobCat='notification', jobDesc='executionSuccess', message='', status='prepare',
                     dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    message = {
        "type": "operation",
        "opname": owner,
        "projectId": projectId,
        "cnotification": {
            "data": "{}",
            "error": "{}",
            "runId": runnerId
        }
    }

    table = dynamodb.Table('notification')
    response = table.put_item(
        Item={
            'id': runnerId,
            'projectId': projectId,
            'showName': showName,
            'status': status,
            'jobDesc': jobDesc,
            'comments': comments,
            'message': json.dumps(message, ensure_ascii=False),
            'jobCat': jobCat,
            'code': code,
            'date': date,
            'category': category,
            'owner': owner
        }
    )
    return response


def create_share_args(event, ts):

    put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], dynamodb=dynamodb)
    conf = event["calculate"]
    tenantIp = event['engine']['dss']['ip']
    ph_conf = {}

    ph_conf.update({"shares": conf.get("shares")})
    ph_conf.update({"company": "pharbers"})
    ph_conf.update({"owner": event["owner"]})
    ph_conf.update({"showName": event["showName"]})
    ph_conf.update({"projectId": event.get("projectId")})
    ph_conf.update({"tenantId": event.get("tenantId")})
    ph_conf.update({"projectName": event.get("projectName")})


    args = {
        "common": {
            "runnerId": event["runnerId"],
            "projectId": event["projectId"],
            "projectName": event["projectName"],
            "owner": event["owner"],
            "showName": event["showName"],
            "tenantId": event["tenantId"]
        },
        "shares": conf.get("shares"),
        "compute_share": {
            "name": "compute_share",
            "type": "spark-submit",
            "clusterId": event["engine"]["id"],
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": [
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
                    "--py-files",
                    "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-4.0.0-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/shareDataSet_dev/share/phjob.py",
                    "s3://ph-platform/2020-11-11/jobs/python/phcli/shareDataSet_dev/share/phmain.py",
                    "--owner",
                    "dev环境",
                    "--dag_name",
                    "share_share_developer",
                    "--run_id",
                    event["runnerId"],
                    "--job_full_name",
                    "share_share_developer_compute_share",
                    "--tenant_ip",
                    tenantIp,
                    "--ph_conf",
                    json.dumps(ph_conf, ensure_ascii=False).replace("}}", "} }").replace("{{", "{ {"),
                ]
            }
        }
    }


    return {
        "args": args,
        "sm": "s3://ph-platform/2020-11-11/jobs/python/phcli/shareDataSet_dev/share/sm_of_share.json"
    }
