import boto3

dynamodb = boto3.resource('dynamodb')

'''
删除所有的dynamodb中的dataset表的索引记录
其中script是上一个lmabda便利出来的详细的需要删除的script记录
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
        "script.$": {
            "id": "",
                ....
        }
    }
'''


def del_dag_item(sortVersion, projectId):

    table = dynamodb.Table("dag")
    table.delete_item(
        Key={
            "projectId": projectId,
            "sortVersion": sortVersion
        },
    )


def lambda_handler(event, context):
    print(event)
    for link in event["links"]:
        del_dag_item(link["sortVersion"], link["projectId"])

    return True
