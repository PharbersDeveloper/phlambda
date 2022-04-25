import boto3
import json

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
            'message': message,
            'jobCat': jobCat,
            'code': code,
            'date': date,
            'category': category,
            'owner': owner
        }
    )
    return response


def create_sample_args(event, ts):

    put_notification(event['runnerId'], event['projectId'], None, 0, "", int(ts), event['owner'], event['showName'], dynamodb=dynamodb)
    conf = event["calculate"]
    ph_conf = {}

    ph_conf.update({"projectName": event.get("projectName")})
    ph_conf.update({"showName": event.get("showName")})

    ph_conf.update({"sourceProjectId": conf.get("sourceProjectId")})
    ph_conf.update({"targetProjectId": conf.get("targetProjectId")})
    ph_conf.update({"datasetId": conf.get("datasetId")})
    ph_conf.update({"datasetName": conf.get("datasetName")})
    ph_conf.update({"sample": conf.get("sample")})
    ph_conf.update({"company": "pharbers"})

    args = {
        "common": {
            "runnerId": event["runnerId"],
            "projectId": event["projectId"],
            "projectName": event["projectName"],
            "owner": event["owner"],
            "showName": event["showName"]
        },
        "compute_sample": {
            "name": "compute_sample",
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
                    "\"spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8\"",
                    "--conf",
                    "\"spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8\"",
                    "--jars",
                    "s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/clickhouse-jdbc-0.2.4.jar,s3://ph-platform/2020-11-11/emr/client/clickhouse-connector/guava-30.1.1-jre.jar",
                    "--py-files",
                    "s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-4.0.0-py3.8.egg,s3://ph-platform/2020-11-11/jobs/python/phcli/sample_sample_developer/sample_sample_developer_compute_sample/phjob.py",
                    "s3://ph-platform/2020-11-11/jobs/python/phcli/sample_sample_developer/sample_sample_developer_compute_sample/phmain.py",
                    "--owner",
                    "dev环境",
                    "--dag_name",
                    "sample_sample_developer",
                    "--run_id",
                    event["runnerId"],
                    "--job_full_name",
                    "sample_sample_developer_compute_sample",
                    "--ph_conf",
                    json.dumps(ph_conf, ensure_ascii=False).replace("}}", "} }").replace("{{", "{ {"),
                ]
            }
        }
    }

    return {
        "args": args,
        "sm": "2020-11-11/jobs/statemachine/pharbers/sample_sample_developer/sample_sample_developer_compute_sample.json"
    }