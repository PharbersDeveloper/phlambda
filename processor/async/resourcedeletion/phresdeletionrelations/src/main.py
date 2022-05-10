import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
'''
这个函数只做一件事情，从输入参数中，按照产品逻辑的到需要删除的脚本与links
核心从dynamodb 的dag表中得到需要删除的关联信息
并将结果详细信息返回，给后面的lambda使用

args:
    event = {
        "traceId.$": "$.common.traceId",
        "projectId.$": "$.common.projectId",
        "owner.$": "$.common.owner",
        "showName.$": "$.common.showName",
        "datasets.$": [
            {
                "name": "555a"
            }
        ],,
        "scripts.$": {
            "jobName": "developer_js1jPtkSmpVCGpw_demo_demo_compute_555a",
        }
    }

return:
    {
        "result": {
            "datasets": {
                "id": "",
                ....
            },
            "stript": {
                "id": "",
                ....
            },
            "links": {
                "id": "",
                ....
            }
        }
    }
'''


def get_dagcof_item_by_sortVersion(projectId, jobName):

    ds_table = dynamodb.Table('dagconf')
    res = ds_table.query(
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("jobName").eq(jobName)
    )
    return res["Items"][0]


def get_dagcof_item_by_jobId(projectId, jobId):

    ds_table = dynamodb.Table('dagconf')
    res = ds_table.query(
        IndexName='dagconf-projectId-id-indexd',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("id").eq(jobId)
    )
    return res["Items"][0]


def get_dag_item_by_name(projectId, name):
    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        IndexName='dag-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").eq(name)
    )

    return res["Items"][0]


def get_dataset_item_by_name(projectId, name):
    ds_table = dynamodb.Table('dataset')
    res = ds_table.query(
        IndexName='dataset-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").eq(name)
    )

    return res["Items"][0]


def get_all_link(projectId):

    ds_table = dynamodb.Table('dag')
    res = ds_table.query(
        IndexName='dag-projectId-name-index',
        KeyConditionExpression=Key("projectId").eq(projectId)
                               & Key("name").eq("empty")
    )
    links = res["Items"]
    return links


def get_node_link(all_links, id):

    del_links = []
    related_node_ids = []

    source_links = list(filter(lambda item: json.loads(item["cmessage"])["sourceId"] == id, all_links))
    target_job_ids = list(json.loads(source_link["cmessage"])["targetId"] for source_link in source_links)
    related_node_ids.extend(target_job_ids)
    del_links.extend(source_links)

    target_links = list(filter(lambda item: json.loads(item["cmessage"])["targetId"] == id, all_links))
    source_job_ids = list(json.loads(target_link["cmessage"])["sourceId"] for target_link in target_links)
    related_node_ids.extend(source_job_ids)
    del_links.extend(target_links)

    return del_links, related_node_ids


def lambda_handler(event, context):

    projectId = event["projectId"]
    # 1 根据dataset script 查找 dag表判断关联关系 返回link表和需要关联删除的job
    # 首先拿出当前projectId下所有的link
    all_del_links = []
    all_del_datasets = []
    all_del_scripts = []
    all_links = get_all_link(projectId)

    # 再判断job的link
    for script in event["scripts"]:
        script_item = get_dagcof_item_by_sortVersion(projectId, script["jobName"])
        del_script_links, related_node_ids = get_node_link(all_links, script_item["id"])
        all_del_links.extend(del_script_links)

    # 再次判断dataset的link
    for dataset in event["datasets"]:
        dag = get_dag_item_by_name(projectId, dataset["name"])
        del_ds_links, related_job_node_ids = get_node_link(all_links, dag["representId"])
        all_del_links.extend(del_ds_links)

    # 根据判断dataset得到的
    for jobId in related_job_node_ids:
        del_related_script_links, related_related_script_ids = get_node_link(all_links, jobId)
        all_del_links.extend(del_related_script_links)

    # 对link进行去重
    deal_all_del_links = []
    for i in all_del_links:
        if i not in deal_all_del_links:
            deal_all_del_links.append(i)

    # 2 查询dataset Name 查询 item
    dataset_items = [get_dataset_item_by_name(projectId, dataset["name"]) for dataset in event["datasets"]]
    all_del_datasets.extend(dataset_items)

    # 3 根据script 的 jobName 查询item
    script_items = [get_dagcof_item_by_sortVersion(projectId, script["jobName"]) for script in event["scripts"]]
    all_del_scripts.extend(script_items)

    # 根据dataset关联job进行 查询item
    related_script_items = [get_dagcof_item_by_jobId(projectId, jobId) for jobId in related_job_node_ids]
    all_del_scripts.extend(related_script_items)

    print(all_del_datasets)
    print(len(all_del_datasets))
    print(all_del_scripts)
    print(len(all_del_scripts))
    print(deal_all_del_links)
    print(len(deal_all_del_links))
    result = {
        "datasets": all_del_datasets,
        "scripts": all_del_scripts,
        "links": deal_all_del_links
    }
    return result

if __name__ == '__main__':
    event = {
        "traceId": "hbzhao_traceId",
        "projectId": "ggjpDje0HUC2JW",
        "owner": "hbzhao_ownerId",
        "showName": "赵浩博",
        "datasets": [
            {
                "name": "111a"
            }
        ],
        "scripts": {

        }
    }
    lambda_handler(event, context=None)