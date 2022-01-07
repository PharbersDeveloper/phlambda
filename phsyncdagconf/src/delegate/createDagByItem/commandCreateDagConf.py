import json

from delegate.createDagByItem.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
from util.AWS import define_value as dv
from delegate.updateAction import UpdateAction
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )


class CommandCreateDagConf(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.dynamodb = DynamoDB()

    def check_outputs(self, dag_conf, dag_conf_list):

        outputs = dag_conf.get("outputs")
        flag = 0
        for dy_dag_conf in dag_conf_list:
            if dy_dag_conf.get("outputs") == outputs:
                # 说明有相同outputs
                raise Exception("output已经被使用")
            else:
                flag = 1
        return flag

    def check_max_index(self, dag_conf):

        projectId = dag_conf.get("projectId")
        inputs = dag_conf.get("inputs")
        input_cats = ["input_index", "uploaded", "intermediate"]
        for input in inputs:
            id = input.get("id")
            data = {
                "table_name": "dataset",
                "key": {
                    "id": id,
                    "projectId": projectId
                }
            }
            res = self.dynamodb.getItem(data)
            cat = res["Item"].get("cat")
            if cat in input_cats:
                check = "ok"
            else:
                raise Exception("inputs选择错误")

        outputs = dag_conf.get("outputs")
        output_cats = ["intermediate", "output_index"]
        for output in outputs:
            id = output.get("id")
            data = {
                "table_name": "dataset",
                "key": {
                    "id": id,
                    "projectId": projectId
                }
            }
            res = self.dynamodb.getItem(data)
            cat = res["Item"].get("cat")
            if cat in output_cats:
                check = "ok"
            else:
                raise Exception("outputs选择错误")
        return check


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
        # 拿到所有的dag_conf后 查询当前dag_conf的输出是否已经被使用
        self.check_outputs(dag_conf, dag_conf_list)
        # print(dag_conf)
        # print(dag_conf_list)

        update_dag_conf_list = self.update_targetId(dag_conf, dag_conf_list)

        return update_dag_conf_list

    def __insert_dagconf(self, action_item):
        # 传递进item_list 包含所有此次event
        data = {}
        data.update({"table_name": "dagconf"})


        dag_conf = json.loads(action_item.get("message"))

        jobId = GenerateID.generate()
        dag_conf.update({"jobId": jobId})
        # 进行input output检查input index只能作为输入，output index 只能作为输出
        self.check_max_index(dag_conf)
        # self.update_targetId(dag_conf)

        targetJobId = []
        dag_conf.update({"targetJobId": json.dumps(targetJobId, ensure_ascii=False)})

        dag_conf.update({"inputs": json.dumps(dag_conf.get("inputs"), ensure_ascii=False)})
        dag_conf.update({"outputs": json.dumps(dag_conf.get("outputs"), ensure_ascii=False)})
        dag_conf.update({"operatorParameters": json.dumps(dag_conf.get("operatorParameters"), ensure_ascii=False)})
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

    def run(self):

        logging.info("运行创建dagConf命令")
        dag_conf_list = self.__insert_dagconf(self.dag_item)

        return dag_conf_list
