import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID


class CreateDag:

    def __init__(self, **kwargs):
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
            job_name = dag_conf.get("jobName")
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

        if dag_item.get("id"):
            cat = "dataset"
            represent_id = dag_item.get("id")
            name = dag_item.get("name")
            cmessage = "<empty>"
            runtime = "intermediate"
        elif dag_item.get("jobId"):
            cat = "job"
            represent_id = dag_item.get("jobId")
            name = dag_item.get("jobName")
            cmessage = dag_item.get("jobName")
            runtime = "python3"
        project_id = dag_conf_list[0].get("projectId")
        flowVersion = dag_conf_list[0].get("flowVersion")
        level = dag_item.get("level")

        ctype = "node"


        data = {}
        data.update({"table_name": "dag"})
        dag_item = {}
        dag_item.update({"name": name})
        dag_item.update({"projectId": project_id})
        dag_item.update({"representId": represent_id})
        dag_item.update({"cmessage": cmessage})
        dag_item.update({"flowVersion": flowVersion})
        dag_item.update({"sortVersion": flowVersion + "_" + represent_id})
        dag_item.update({"cat": cat})
        dag_item.update({"runtime": runtime})
        dag_item.update({"ctype": ctype})
        dag_item.update({"level": str(level)})
        position = {
            "x": "0",
            "y": "0",
            "z": "0",
            "w": "0",
            "h": "0",
        }
        dag_item.update({"position": json.dumps(position)})
        data.update({"item": dag_item})
        # print("job node ====================================")
        # print(data)
        # self.dynamodb.putData(data)


        return dag_item

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
            dag_data = self.create_node(json.loads(dag_item), dag_conf_list)
            dag_data_list.append(dag_data)

        dag_list.extend(dag_data_list)


        return dag_list
