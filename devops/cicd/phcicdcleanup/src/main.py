import json
import boto3
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
'''
将错误提取出来写入到notification中
args:
    event = {
                "projectId": "ggjpDje20HUC2JW",
                "traceId": "",
                "projectName": "demo",
                "owner": "alfred",
                "showName": "alfred",
                "errors": {
                }
            },
return:
    {
        "type": "notification",
        "opname": event["owner"],
        "cnotification": {
            "data": {},
            "error": errors
    }
}
'''


def copy_manage_resource(bucket_name, prefix):
    copy_source = {
        'Bucket': bucket_name,
        'Key': prefix + "/manage_back.yaml"
    }
    s3_resource.meta.client.copy(copy_source, bucket_name, prefix + "/manage.yaml")


def del_s3_resource(bucket, key):
    response = s3_client.delete_object(
        Bucket=bucket,
        Key=key
    )


def lambda_handler(event, context):
    print(event)
    # 如果创建失败 则删除cloudformation 同时删除s3上cicd/prefix/manage.yaml
    # 判断processor 和trigger 里面的required是否为true
    if event["processor"]["required"]:
        del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["processor"]["prefix"] + "/manage.yaml")
        # 判断这次操作是不是update操作
        if event["processorMetadata"]["changeSetMsg"]["changeSetName"]:
            # 如果update失败 将cicd/prefix/manage_back.yaml 文件恢复到manage.yaml文件
            copy_manage_resource("ph-platform", "2020-11-11/cicd/" + event["processor"]["prefix"])
            del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["processor"]["prefix"] + "/manage_back.yaml")
    if event["trigger"]["required"]:
        del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["trigger"]["prefix"] + "/manage.yaml")
        # 判断这次操作是不是update操作
        if event["triggerMetadata"]["changeSetMsg"]["changeSetName"]:
            # 如果update失败 将cicd/prefix/manage_back.yaml 文件恢复到manage.yaml文件 删除manage_back文件
            copy_manage_resource("ph-platform", "2020-11-11/cicd/" + event["trigger"]["prefix"])
            del_s3_resource("ph-platform", "2020-11-11/cicd/" + event["trigger"]["prefix"] + "/manage_back.yaml")


    return 1
