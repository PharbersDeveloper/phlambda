import json

from delegate.createDagByItem.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )


class CommandCreateDag(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.dynamodb = DynamoDB()

    def create_link(self, dag_conf):
        """
        根据 dag_conf 的列表 分別创建每个dag_conf对应的link
        :param dag_conf: dag的详细参数的列表
        :return: 创建link成功后返回一条消息
        """
        def create_link_list(messages):
            link_list = []
            for message in messages:
                represent_id = GenerateID.generate()
                data = {}
                data.update({"table_name": "dag"})
                item = {}
                item.update({"representId": represent_id})
                item.update({"flowVersion": dag_conf.get("flowVersion")})
                item.update({"sortVersion": dag_conf.get("flowVersion") + "_" + represent_id})
                item.update({"projectId": dag_conf.get("projectId")})
                item.update({"ctype": "link"})
                item.update({"cat": "null"})
                item.update({"name": "null"})
                item.update({"cmessage": json.dumps(message, ensure_ascii=False)})
                data.update({"item": item})
                data.update({"position": "null"})
                data.update({"level": "null"})
                data.update({"runtime": "null"})
                link_list.append(item)

            return link_list

        def create_source_target_map(dag_conf):
            job_id = dag_conf.get("jobId")
            job_name = dag_conf.get("jobShowName")
            id_maps = []
            for input in json.loads(dag_conf.get("inputs")):
                id_map = {}
                id_map.update({"sourceId": input.get("id")})
                id_map.update({"sourceName": input.get("name")})
                id_map.update({"targetId": job_id})
                id_map.update({"targetName": job_name})
                id_maps.append(id_map)
            for output in json.loads(dag_conf.get("outputs")):
                id_map = {}
                id_map.update({"sourceId": job_id})
                id_map.update({"sourceName": job_name})
                id_map.update({"targetId": output.get("id")})
                id_map.update({"targetName": output.get("name")})
                id_maps.append(id_map)

            return id_maps

        messages = create_source_target_map(dag_conf)
        link_list = create_link_list(messages)

        return link_list

    def create_node(self, dag_item, dag_conf_list):

        """
        根据 dag_conf 的列表 分別创建每个job 对应的node
        :param dag_conf_list: dag的详细参数的列表
        :return: 创建job_node成功后返回一条消息
        """
        def get_job_runtime(dag_item, dag_conf_list):
            for dag_conf in dag_conf_list:
                if dag_item.get("jobId") == dag_conf.get("jobId"):
                    runtime = dag_conf.get("runtime")
            return runtime

        def get_ds_prop(id, projectId):
            data = {}
            data.update({"table_name": "dataset"})
            key = {
                "id": id,
                "projectId": projectId
            }
            data.update({"key":key})
            res = self.dynamodb.getItem(data)
            prop = res["Item"].get("prop")
            return prop

        def create_ds_item(dag_item, dag_conf_list):
            project_id = dag_conf_list[0].get("projectId")
            flowVersion = dag_conf_list[0].get("flowVersion")
            name = dag_item.get("name")
            represent_id = dag_item.get("id")
            level = dag_item.get("level")
            # 获取ds的 prop
            prop = get_ds_prop(represent_id, project_id)
            cat = "dataset"
            ctype = "node"
            cmessage = "<empty>"

            data = {"table_name": "dataset"}
            key = {
                "id": represent_id,
                "projectId": project_id,
            }
            data.update({"key": key})

            while data:
                res = self.dynamodb.getItem(data)
                if res.get("Item"):
                    runtime = res["Item"].get("cat", "uploaded")

                    break

            process_dag_item = {}
            process_dag_item.update({"name": name})
            process_dag_item.update({"prop": prop})
            process_dag_item.update({"projectId": project_id})
            process_dag_item.update({"representId": represent_id})
            process_dag_item.update({"cmessage": cmessage})
            process_dag_item.update({"flowVersion": flowVersion})
            process_dag_item.update({"sortVersion": flowVersion + "_" + represent_id})
            process_dag_item.update({"cat": cat})
            process_dag_item.update({"runtime": runtime})
            process_dag_item.update({"ctype": ctype})
            process_dag_item.update({"level": str(level)})
            position = {
                "x": "0",
                "y": "0",
                "z": "0",
                "w": "0",
                "h": "0",
            }
            process_dag_item.update({"position": json.dumps(position)})

            return process_dag_item

        def create_job_item(dag_item, dag_conf_list):
            represent_id = dag_item.get("jobId")
            name = dag_item.get("jobName")
            cmessage = dag_item.get("jobName")
            runtime = get_job_runtime(dag_item, dag_conf_list)
            project_id = dag_conf_list[0].get("projectId")
            flowVersion = dag_conf_list[0].get("flowVersion")
            operatorParameters = dag_item.get("operatorParameters")
            level = dag_item.get("level")
            ctype = "node"
            cat = "job"

            process_dag_item = {}
            process_dag_item.update({"name": name})
            process_dag_item.update({"prop": "<empty>"})
            process_dag_item.update({"projectId": project_id})
            process_dag_item.update({"representId": represent_id})
            process_dag_item.update({"cmessage": cmessage})
            process_dag_item.update({"flowVersion": flowVersion})
            process_dag_item.update({"operatorParameters": operatorParameters})
            process_dag_item.update({"sortVersion": flowVersion + "_" + represent_id})
            process_dag_item.update({"cat": cat})
            process_dag_item.update({"runtime": runtime})
            process_dag_item.update({"ctype": ctype})
            process_dag_item.update({"level": str(level)})
            position = {
                "x": "0",
                "y": "0",
                "z": "0",
                "w": "0",
                "h": "0",
            }
            process_dag_item.update({"position": json.dumps(position)})

            return process_dag_item

        if dag_item.get("id"):
            process_dag_item = create_ds_item(dag_item, dag_conf_list)
        elif dag_item.get("jobId"):
            process_dag_item = create_job_item(dag_item, dag_conf_list)

        return process_dag_item

    def create_dag(self, dag_item_list, dag_conf_list):

        """
        创建 dag link
        :param dag_conf_list: dag的详细参数的列表
        """
        # level_maps = self.determine_node_level(dag_conf)
        dag_list = []
        # 根据创建 event 下所有的dag_conf 创建link
        link_data_list = []
        for dag_conf in dag_conf_list:
            link_list = self.create_link(dag_conf)
            link_data_list.extend(link_list)

        dag_list.extend(link_data_list)

        dag_data_list = []
        for dag_item in dag_item_list:
            print(dag_item)
        for dag_item in dag_item_list:
            print(dag_item)
            dag_data = self.create_node(json.loads(dag_item), dag_conf_list)
            dag_data_list.append(dag_data)

        dag_list.extend(dag_data_list)

        return dag_list

    def run(self):

        logging.info("运行创建dag命令")
        dag_data = self.create_dag(self.dag_item_level_list, self.dag_conf_list)
        return dag_data
