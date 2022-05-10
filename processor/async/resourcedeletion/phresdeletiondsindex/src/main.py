import boto3

dynamodb = boto3.resource('dynamodb')
'''
删除所有的dynamodb中的dataset表的索引记录
其中datasets是上一个lmabda便利出来的详细的需要删除的datasets记录
resources 为从ssm中读取的数据

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "projectName.$": "$.common.projectName",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "resources": {
    
        },
        "datasets.$": [{
            "id": "",
                ....
        }]
    }
'''


def del_dataset_item(dsId, projectId):

    table = dynamodb.Table("dataset")
    table.delete_item(
        Key={
            "id": dsId,
            "projectId": projectId
        },
    )


def lambda_handler(event, context):

    for dataset in event["dataset"]:
        del_dataset_item(dataset["id"], dataset["projectId"])

    return True
