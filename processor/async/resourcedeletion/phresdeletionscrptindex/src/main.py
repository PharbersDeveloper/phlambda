import boto3

dynamodb = boto3.resource('dynamodb')

'''
删除所有的dynamodb中的dataset表的索引记录
其中 links 是上一个lambda便利出来的详细的需要删除的 dag 表中的记录，包括node 和 link
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
        "links.$": [{
            "id": "",
                ....
        }]
    }
'''


def del_dagconf_item(jobName, projectId):

    table = dynamodb.Table("dataset")
    table.delete_item(
        Key={
            "jobName": jobName,
            "projectId": projectId
        },
    )


def lambda_handler(event, context):

    for script in event["scripts"]:
        del_dagconf_item(script["jobName"], script["projectId"])

    return True