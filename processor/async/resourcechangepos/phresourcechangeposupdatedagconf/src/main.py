import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')

'''
将错误提取出来写入到notification中
args:
    args:
    event = {
        "traceId": "traceId",
        "projectId": "projectId",
        "projectName": "projectName",
        "owner": "owner",
        "showName": "showName",
        "script": {
            "old": {
                "name": compute_A_out,
                "id": "22jpN8YtMIhGTnW"
            },
            "new": {
                "name": "compute_B_out",
                "runtime": "python",
                "inputs": "[\"B\"]",
                "output": "B_out"
            }
        }   
    },
return:
    {
        "deleteItems":[
            {}
        ],
        "insertItems":[
            {}
        ]
    }
}
'''
def get_dagconf_item(projectId, jobId):
    dagconf_table = dynamodb.Table('dagconf')
    res = dagconf_table.query(
        IndexName='dagconf-projectId-id-indexd',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("id").eq(jobId)
    )

    return res.get("Items")[0]


def lambda_handler(event, context):
    print(event)
    script = event["script"]
    deleteItems = []
    insertItems = []
    # 查询dag_conf item
    # 修改jobName, actionName, jobDisplayName, jobPath, jobShowName, output, inputs, traceId
    delDagconfItem = get_dagconf_item(event["projectId"], event["script"]["old"]["id"])
    deleteItems.append(delDagconfItem)

    newJobName = delDagconfItem.get("jobName").replace(script["old"]["name"], script["new"]["name"])
    newActionName = delDagconfItem.get("actionName").replace(script["old"]["name"], script["new"]["name"])
    newJobDisplayName = delDagconfItem.get("jobDisplayName").replace(script["old"]["name"], script["new"]["name"])
    newJobPath = delDagconfItem.get("jobPath").replace(script["old"]["name"], script["new"]["name"])
    newJobShowName = delDagconfItem.get("jobShowName").replace(script["old"]["name"], script["new"]["name"])

    newTraceId = event["traceId"]
    newOwnerd = event["owner"]
    newShowName = event["showName"]
    newOutput = script["new"]["output"]
    newInputs = script["new"]["inputs"]

    newDagconfItem = delDagconfItem.copy()
    newDagconfItem.update({
        "jobName": newJobName,
        "actionName": newActionName,
        "jobDisplayName": newJobDisplayName,
        "jobPath": newJobPath,
        "jobShowName": newJobShowName,
        "inputs": newInputs,
        "outputs": newOutput,
        "owner": newOwnerd,
        "showName": newShowName,
        "traceId": newTraceId,
        "prop": script["new"]["prop"]
    })
    insertItems.append(newDagconfItem)
    return {
        "deleteItems": deleteItems,
        "insertItems": insertItems
    }
