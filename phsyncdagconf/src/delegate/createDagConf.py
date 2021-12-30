import json
import logging

from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
from util.AWS import define_value as dv
from delegate.updateAction import UpdateAction

class CreateDagConf:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def check_outputs(self, dag_conf):

        outputs = dag_conf.get("outputs")
        
        data = {}
        data.update({"table_name": "dagconf"})
        attribute = {
            "key": "outputs",
            "value": json.dumps(outputs, ensure_ascii=False)
        }
        data.update({"attribute": attribute})
        res = self.dynamodb.query_attribute(data)
        if res.get("Items"):
            # 说明有相同outputs
            raise Exception("output已经被使用")
        else:
            return 0

    def update_targetId(self, dag_conf, dag_conf_list):


        if dag_conf.get("inputs"):
            # 判断input 如果是某个item的output
            # 则将当前jobId 添加到input Item 的targetJobId
            for dy_dag_conf in dag_conf_list:
                for input in json.loads(dag_conf.get("inputs")):
                    # 如果当前 dag_conf的 input 是某个item的outputs 说明是item的 targetjob 更新item
                    if json.dumps(input, ensure_ascii=False) in dy_dag_conf.get("outputs"):
                        # 更新 item 的 targetId
                        dy_targetJobId_list = eval(dy_dag_conf.get("targetJobId"))
                        dy_targetJobId_list.append(dag_conf.get("jobId"))
                        dy_dag_conf["targetJobId"] = json.dumps(dy_targetJobId_list, ensure_ascii=False)

            # 判断输出 是某个item的input
            for dy_dag_conf in dag_conf_list:
                output = json.loads(dag_conf.get("outputs"))[0]
                if json.dumps(output, ensure_ascii=False) in dy_dag_conf.get("inputs"):
                    targetJobId_list = eval(dag_conf.get("targetJobId"))
                    targetJobId_list.append(dy_dag_conf.get("jobId"))
                    dag_conf["targetJobId"] = json.dumps(targetJobId_list, ensure_ascii=False)

            # 修改好targetId 后 将当前dag_conf 连接到dag_conf list
            dag_conf_list.append(dag_conf)
        return dag_conf_list

    def get_all_dag_conf(self, dag_conf):
        projectId = dag_conf.get("projectId")
        flowVersion = dag_conf.get("flowVersion")
        data = {}
        data.update({"table_name": "dagconf"})
        data.update({"partition_key": "projectId"})
        data.update({"partition_value": projectId})
        data.update({"sort_key": "jobName"})
        data.update({"sort_value": flowVersion})
        res = self.dynamodb.queryTableBeginWith(data)
        dag_conf_list = []
        for dy_dag_conf in res.get("Items"):
            dag_conf_list.append(dy_dag_conf)
        # print(dag_conf)
        # print(dag_conf_list)

        update_dag_conf_list = self.update_targetId(dag_conf, dag_conf_list)

        return update_dag_conf_list

    def insert_dagconf(self, action_item):

        # 传递进item_list 包含所有此次event
        data = {}
        data.update({"table_name": "dagconf"})


        dag_conf = json.loads(action_item.get("message"))

        jobId = GenerateID.generate()
        dag_conf.update({"jobId": jobId})
        # 进行outputs检查
        # self.check_outputs(dag_conf)
        # self.update_targetId(dag_conf)

        targetJobId = []
        dag_conf.update({"targetJobId": json.dumps(targetJobId, ensure_ascii=False)})

        dag_conf.update({"inputs": json.dumps(dag_conf.get("inputs"), ensure_ascii=False)})
        dag_conf.update({"outputs": json.dumps(dag_conf.get("outputs"), ensure_ascii=False)})
        job_full_name = dag_conf.get("flowVersion") + "_" + \
                        dag_conf.get("jobId") + "_" + \
                        dag_conf.get("projectName") + "_" + \
                        dag_conf.get("dagName") + "_" + \
                        dag_conf.get("jobName")
        job_display_full_name = dag_conf.get("projectName") + "_" + \
                        dag_conf.get("dagName") + "_" + \
                        dag_conf.get("flowVersion") + "_" + \
                        dag_conf.get("jobName") + "_" + \
                        dag_conf.get("jobId")
        dag_conf.update({"jobShowName": dag_conf.get("jobName")})
        dag_conf.update({"jobName": job_full_name})
        dag_conf.update({"jobDisplayName": job_display_full_name })
        dag_conf.update({"labels": json.dumps(dag_conf.get("labels"), ensure_ascii=False)})
        dag_conf.update({"projectName": dag_conf.get("projectName")})
        dag_conf.update({"id": GenerateID.generate()})

        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")
        job_path = dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + dag_name + "/" + job_display_full_name + "/phjob.py"
        dag_conf.update({"jobPath": job_path})
        data.update({"item": dag_conf})

        update_dag_conf_list = self.get_all_dag_conf(dag_conf)


        return update_dag_conf_list

    def refresh_dagconf(self, action_item):
        dag_conf = json.loads(action_item.get("message"))
        dag_conf_list = self.get_all_dag_conf(dag_conf)

        return dag_conf_list