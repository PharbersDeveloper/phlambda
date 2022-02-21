import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID

class CreateDagConf:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def insert_dagconf(self, item_list):
        # 传递进item_list 包含所有此次event
        dag_conf_list = []
        for action_item in item_list:
            dag_conf = json.loads(action_item.get("message"))
            data = {}
            data.update({"table_name": "dagconf"})
            dag_conf.update({"inputs": json.dumps(dag_conf.get("inputs"))})
            dag_conf.update({"outputs": json.dumps(dag_conf.get("outputs"))})
            data.update({"item": dag_conf})
            job_full_name = dag_conf.get("jobId") + "_" + \
                            dag_conf.get("projectName") + "_" + \
                            dag_conf.get("dagName") + "_" + \
                            dag_conf.get("flowVersion") + "_" + \
                            dag_conf.get("jobName")
            job_display_full_name = dag_conf.get("projectName") + "_" + \
                            dag_conf.get("dagName") + "_" + \
                            dag_conf.get("flowVersion") + "_" + \
                            dag_conf.get("jobName") + "_" + \
                            dag_conf.get("jobId")
            dag_conf.update({"jobName": job_full_name })
            dag_conf.update({"jobDisplayName": job_display_full_name})
            dag_conf.update({"id": GenerateID.generate()})
            dag_conf.update({"labels": json.dumps(dag_conf.get("labels"))})

            # print("dagconf =======================================")
            # print(data)
            # self.dynamodb.putData(data)
            dag_conf_list.append(dag_conf)
        return dag_conf_list
