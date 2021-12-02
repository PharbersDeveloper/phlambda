import json

from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
from util.AWS import define_value as dv
from delegate.updateAction import UpdateAction
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )

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

    def update_targetId(self, dag_conf):
        # 判断input 如果是某个item的output
        # 则将当前jobId 添加到input Item 的targetJobId
        data = {}
        data.update({"table_name": "dagconf"})
        data.update({"partition_key": "projectId"})
        data.update({"partition_value": dag_conf.get("projectId")})
        data.update({"sort_key": "jobName"})
        data.update({"sort_value": dag_conf.get("flowVersion")})
        res = self.dynamodb.queryTableBeginWith(data)
        if res.get("Items"):
            for item in res.get("Items"):
                for input in dag_conf.get("inputs"):
                    # 如果当前 dag_conf的 input 是某个item的outputs 说明是item的 targetjob 更新item
                    if json.dumps(input, ensure_ascii=False) in item.get("outputs"):
                        # 更新 item 的 targetId
                        targetJobId_list = eval(item.get("targetJobId"))
                        targetJobId_list.append(dag_conf.get("jobId"))
                        item["targetJobId"] = json.dumps(targetJobId_list, ensure_ascii=False)
                        # 更新 item
                        UpdateAction().updateDagConf(item)


    def get_targetId(self, dag_conf):
        # 判断输出 是某个item的input
        data = {}
        data.update({"table_name": "dagconf"})
        data.update({"partition_key": "projectId"})
        data.update({"partition_value": dag_conf.get("projectId")})
        data.update({"sort_key": "jobName"})
        data.update({"sort_value": dag_conf.get("flowVersion")})
        res = self.dynamodb.queryTableBeginWith(data)
        targetJobId = []
        if res.get("Items"):
            for item in res.get("Items"):
                output = dag_conf.get("outputs")[0]
                if json.dumps(output, ensure_ascii=False) in item.get("inputs"):
                    targetJobId.append(item.get("jobId"))

        return targetJobId


    def insert_dagconf(self, action_item):
        # 传递进item_list 包含所有此次event
        data = {}
        data.update({"table_name": "dagconf"})

        dag_conf = json.loads(action_item.get("message"))
        jobId = GenerateID.generate()
        dag_conf.update({"jobId": jobId})
        # 进行outputs检查
        self.check_outputs(dag_conf)
        self.update_targetId(dag_conf)
        targetJobId = self.get_targetId(dag_conf)
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
        dag_conf.update({"jobName": job_full_name })
        dag_conf.update({"jobDisplayName": job_display_full_name })
        dag_conf.update({"labels": json.dumps(dag_conf.get("labels"), ensure_ascii=False)})
        dag_conf.update({"projectName": dag_conf.get("projectName")})
        dag_conf.update({"id": GenerateID.generate()})

        dag_name = dag_conf.get("projectName") + \
                   "_" + dag_conf.get("dagName") + \
                   "_" + dag_conf.get("flowVersion")
        job_path = dv.S3_PREFIX + dv.TEMPLATE_BUCKET + "/" + dv.CLI_VERSION + dv.DAGS_S3_PHJOBS_PATH + dag_name + "/" + job_display_full_name + "/phjob.py"
        dag_conf.update({"jobPath": job_path})


        data.update({"item": dag_conf})
        # print("dagconf =======================================")
        # print(data)
        # self.dynamodb.putData(data)
        return dag_conf

    def exec(self, dag_conf):
        logging.info(dag_conf)
        logging.info("运行创建dagConf命令")