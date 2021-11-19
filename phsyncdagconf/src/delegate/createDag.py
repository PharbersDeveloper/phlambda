import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID


class CreateDag:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def get_dataset_represent_id(self, dag_conf):
        """
        根据 dag_conf 获取所有 source_dataset_id, target_dataset_id
        :param dag_conf: dag的详细参数
        :return: 包含 source_dataset_ids, target_dataset_ids的一个dict
        """
        def get_input_dateset_id(inputs):
            return [inputs.get(key) for key in inputs.keys()]

        def get_output_dateset_id(outputs):
            return [outputs.get(key) for key in outputs.keys()]

        source_dataset_ids = get_input_dateset_id(json.loads(dag_conf.get("inputs")))
        target_dataset_ids = get_output_dateset_id(json.loads(dag_conf.get("outputs")))

        return {
            "source_dataset_ids": source_dataset_ids,
            "target_dataset_ids": target_dataset_ids
        }

    def create_link(self, dag_conf_list):
        """
        根据 dag_conf 的列表 分別创建每个dag_conf对应的link
        :param dag_conf_list: dag的详细参数的列表
        :return: 创建link成功后返回一条消息
        """
        def put_link_to_database(messages):
            for message in messages:
                data = {}
                data.update({"table_name": "dag"})
                item = {}
                item.update({"representId": GenerateID.generate()})
                item.update({"projectId": dag_conf.get("project_id")})
                item.update({"ctype": "link"})
                item.update({"cat": None})
                item.update({"name": None})
                item.update({"cmessage": json.dumps(message)})
                data.update({"item": item})
                data.update({"position": None})
                data.update({"level": None})
                print(data)
                # self.dynamodb.putData(data)

        def create_source_target_map(represent_ids):
            job_id = dag_conf.get("job_id")
            id_maps = []
            for key, value in represent_ids.items():
                if key == "source_dataset_ids":
                    for source_id in value:
                        id_map = {}
                        id_map.update({"sourceId": source_id})
                        id_map.update({"targetId": job_id})
                        id_maps.append(id_map)
                else:
                    for target_id in value:
                        id_map = {}
                        id_map.update({"sourceId": job_id})
                        id_map.update({"targetId": target_id})
                        id_maps.append(id_map)
            return id_maps

        for dag_conf in dag_conf_list:
            represent_ids = self.get_dataset_represent_id(dag_conf)
            messages = create_source_target_map(represent_ids)
            put_link_to_database(messages)

        return "create link success"

    def create_job_node(self, dag_conf_list):
        """
        根据 dag_conf 的列表 分別创建每个job 对应的node
        :param dag_conf_list: dag的详细参数的列表
        :return: 创建job_node成功后返回一条消息
        """
        for dag_conf in dag_conf_list:
            project_id = dag_conf.get("projectId")
            represent_id = dag_conf.get("jobId")
            cat = "job"
            ctype = "node"
            name = dag_conf.get("dagName") \
                   + "_" + dag_conf.get("flowVersion") \
                   + "_" + dag_conf.get("jobName") \
                   + "_" + dag_conf.get("jobVersion")
            data = {}
            data.update({"table_name": "dag"})
            dag_item = {}
            dag_item.update({"projectId": project_id})
            dag_item.update({"representId": represent_id})
            dag_item.update({"cmessage": name})
            dag_item.update({"cat": cat})
            dag_item.update({"ctype": ctype})
            dag_item.update({"name": name})
            dag_item.update({"level": "2"})
            dag_item.update({"position": "(0,0)"})
            data.update({"item": dag_item})
            print(data)
            # self.dynamodb.putData(data)

        return "create job_node success"

    def create_dataset_node(self, dag_conf_list):
        """
        根据 dag_conf 的列表 分別创建每个dataset 对应的node
        :param dag_conf_list: dag的详细参数的列表
        :return: 创建dataset_node成功后返回一条消息
        """
        def create_dataset_node(data, item, dag_conf, ds_type, ds_level):
            for key, value in json.loads(dag_conf.get(ds_type)).items():
                item.update({"representId": value})
                item.update({"name": key})
                item.update({"level": ds_level})
                data.update({"item": item})
                # self.dynamodb.putData(data)
                print(data)

        def create_output_dataset_node(data, item, dag_conf):
            for key, value in json.loads(dag_conf.get("outputs")).items():
                item.update({"representId": value})
                item.update({"name": key})
                item.update({"level": "3"})
                data.update({"item": item})
                # self.dynamodb.putData(data)
                print(data)

        for dag_conf in dag_conf_list:
            data = {}
            item = {}
            data.update({"table_name": "dag"})
            item.update({"projectId": dag_conf.get("project_id")})
            item.update({"cat": "dataset"})
            item.update({"ctype": "node"})
            item.update({"position": "(0,0)"})
            create_dataset_node(data, item, dag_conf, ds_type="inputs", ds_level="1")
            create_dataset_node(data, item, dag_conf, ds_type="outputs", ds_level="3")

        return ""

    def create_node(self, dag_conf_list):

        # 创建dataset的node
        self.create_dataset_node(dag_conf_list)
        # 创建job的node
        self.create_job_node(dag_conf_list)

    def create_dag(self, dag_conf_list):

        # 根据创建 event 下所有的dag_conf 创建link
        self.create_link(dag_conf_list)

        self.create_node(dag_conf_list)
