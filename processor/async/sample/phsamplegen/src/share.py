import boto3
import json

'''
args = {
    "common": {
        "tranceId": "",
        "runnerId": "sample_sample_developer_2022-07-04T05:49:39+00:00",
        "projectId": "Dp10sMiAYXWxRZj",
        "projectName": "sample",
        "owner": "16dc4eb5-5ed3-4952-aaed-17b3cc5f638b",
        "showName": "赵浩博",
        "tenantId": "zudIcG_17yj8CEUoCTHg"
    },
    "shares": [
        {
            "target": "ds name", // 共享时的目标DS 名称
            "targetCat": "catalog | intermediate | uploaded", // 共享时的目标DS的类型  catalog是数据目录  intermediate是结果数据集  uploaded 是上传的数据 都需要分别处理
            "targetPartitionKeys": [
                {
                    "name": "key1",
                    "type": "string"
                },
                {
                    "name": "key2",
                    "type": "string"
                }
            ],
            "sourceSelectVersions": ["version1", "version2", "version3"]
            "source": "ds name", // 共享时的源DS 名称
        }
    ]
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
            "showName": event["showName"]
        },
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
