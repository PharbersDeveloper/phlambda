import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
from util.AWS import define_value as dv

class CreateDagConf:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def check_outputs(self, dag_conf):

        outputs = dag_conf.get("outputs")

        data = {}
        data.update({"table_name": "dagconf"})
        attribute = {
            "key": "outputs",
            "value": json.dumps(outputs)
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
        inputs = dag_conf.get("inputs")
        for input in inputs:
            data = {}
            data.update({"table_name": "dagconf"})
            input_list = []
            input_list.append(input)
            attribute = {
                "key": "outputs",
                "value": json.dumps(input_list)
            }
            data.update({"attribute": attribute})
            res = self.dynamodb.query_attribute(data)
            print(res)


    def get_targetId(self):
        pass


    def insert_dagconf(self, action_item):
        # 传递进item_list 包含所有此次event

        dag_conf = json.loads(action_item.get("message"))
        jobId = GenerateID.generate()
        # 进行outputs检查
        # self.check_outputs(dag_conf)
        self.update_targetId(dag_conf)
        data = {}
        data.update({"table_name": "dagconf"})
        dag_conf.update({"inputs": json.dumps(dag_conf.get("inputs"))})
        dag_conf.update({"outputs": json.dumps(dag_conf.get("outputs"))})
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
        dag_conf.update({"labels": json.dumps(dag_conf.get("labels"))})
        dag_conf.update({"projectName": dag_conf.get("projectName")})
        dag_conf.update({"id": GenerateID.generate()})
        dag_conf.update({"jobId": jobId})
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
