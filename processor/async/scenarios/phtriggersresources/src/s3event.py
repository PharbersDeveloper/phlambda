
import uuid
import boto3
import json
import time

s3 = boto3.resource('s3')


def get_uuid():
    uu_id = uuid.uuid4()
    suu_id = ''.join(str(uu_id).split('-'))
    return suu_id


def s3_bucket_notification(**kwargs):
    projectId = kwargs.get("projectId")
    dsNames = kwargs.get("dsNames")
    notif_args = list(map(lambda ds_name: {
        'Id': f'{get_uuid()}',
        'TopicArn': 'arn:aws-cn:sns:cn-northwest-1:444603803904:PH_NOTICE_S3',
        'Events': ['s3:ObjectCreated:Put'],
        'Filter': {'Key': {'FilterRules': [{
            'Name': 'prefix',
            'Value': f'2020-11-11/lake/pharbers/{projectId}/{ds_name}/'}]}}
                    }, dsNames))

    bucket_notification = s3.BucketNotification('ph-platform')
    response = bucket_notification.put(
        NotificationConfiguration={
            'TopicConfigurations': notif_args
        },
        SkipDestinationValidation=True
    )


def wirte_s3(tenantId, projectId, projectName, owner, showName, scenarioId, dsNames, **kwargs):
    for dsName in dsNames:
        bucket = s3.Bucket("ph-platform")
        try:
            response = json.loads(bucket.get_object(Key=f"2020-11-11/lake/pharbers/{projectId}/{dsName}/__resource.json").get('Body').read())
        except:
            response = []
        s3_body = json.dumps(response.append({
            "tenantId": tenantId,
            "projectId": projectId,
            "projectName": projectName,
            "owner": owner,
            "showName": showName,
            "scenarioId": scenarioId,
        }))
        bucket.put_object(Body=s3_body, Key=f"2020-11-11/lake/pharbers/{projectId}/{dsName}/__resource.json")


def dataset(trigger, **kwargs):
    print(trigger)
    wirte_s3(**trigger)
    time.sleep(1)
    s3_bucket_notification(**trigger)
    return True



# # args = {"projectId": "ggjpDje0HUC2JW", "dsNames": ["1112"]}
# # s3_bucket_notification(**args)
#
# # bucket_notification = s3.BucketNotification('ph-platform')
# # print(bucket_notification.load())
# #
# #
# client = boto3.client('s3')
# response = client.get_bucket_notification_configuration(
#     Bucket='ph-platform',
# )
# print(response["TopicConfigurations"])
