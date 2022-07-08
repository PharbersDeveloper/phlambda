
import boto3
import json
import time

s3 = boto3.resource('s3')


def bucket_notif_args(projectId, dsNames, **kwargs):
    return list(map(lambda ds_name : {
            'Id': f'{projectId}{ds_name}',
            # 'Id': f'test',
            'TopicArn': 'arn:aws-cn:sns:cn-northwest-1:444603803904:PH_NOTICE_S3',
            'Events': ['s3:ObjectCreated:Put'],
            'Filter': {'Key': {'FilterRules': [{
                            'Name': 'prefix',
                            'Value': f'2020-11-11/lake/pharbers/{projectId}/{ds_name}/'}]}}
            }, dsNames))


def s3_bucket_notification(**kwargs):
    bucket_notification = s3.BucketNotification('ph-platform')
    print(bucket_notif_args(**kwargs))
    response = bucket_notification.put(
        NotificationConfiguration={
            'TopicConfigurations': bucket_notif_args(**kwargs)
        },
        SkipDestinationValidation=True
    )


def wirte_s3(tenantId, projectId, projectName, owner, showName, scenarioId, dsNames, **kwargs):
    for dsName in dsNames:
        s3_body = json.dumps([{
            "tenantId": tenantId,
            "projectId": projectId,
            "projectName": projectName,
            "owner": owner,
            "showName": showName,
            "scenarioId": scenarioId,
        }])
        bucket = s3.Bucket("ph-platform")
        bucket.put_object(Body=s3_body, Key=f"2020-11-11/lake/pharbers/{projectId}/{dsName}/__resource.json")


def dataset(trigger):
    print(trigger)
    wirte_s3(**trigger)
    time.sleep(1)
    s3_bucket_notification(**trigger)
    return True
