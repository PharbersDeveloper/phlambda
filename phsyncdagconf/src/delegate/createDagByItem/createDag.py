import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )

class CreateDag:

    def __init__(self, **kwargs):
        self.dynamodb = DynamoDB()

    def get_max_level(self, table_name, partition_key, partition_value):
        data = {}
        data["table_name"] = table_name
        data["partition_key"] = partition_key
        data["partition_value"] = partition_value
        res = self.dynamodb.queryTable(data)
        items = res.get("Items")
        level_list = []
        for item in items:
            level = item.get("level", None)
            if type(level) == str:
                level_list.append(int(level))

        if len(level_list) == 0:
            max_level = 0
        else:
            max_level = max(level_list)

        return max_level

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

    def create_link(self, dag_conf):
        """
        根据 dag_conf 的列表 分別创建每个dag_conf对应的link
        :param dag_conf: dag的详细参数的列表
        :return: 创建link成功后返回一条消息
        """
        def put_link_to_database(messages):
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
                item.update({"cat": None})
                item.update({"name": None})
                item.update({"cmessage": json.dumps(message, ensure_ascii=False)})
                data.update({"item": item})
                data.update({"position": None})
                data.update({"level": None})
                data.update({"runtime": None})
                # print("dag link ========================================")
                # print(data)
                # self.dynamodb.putData(data)
                link_list.append(data)

            return link_list

        def create_source_target_map(dag_conf):
            job_id = dag_conf.get("jobId")
            job_name = dag_conf.get("jobDisplayName")
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

        # represent_ids = self.get_dataset_represent_id(dag_conf)
        messages = create_source_target_map(dag_conf)
        link_list = put_link_to_database(messages)

        return link_list

    def create_job_node(self, dag_conf, level_maps):
        """
        根据 dag_conf 的列表 分別创建每个job 对应的node
        :param dag_conf_list: dag的详细参数的列表
        :return: 创建job_node成功后返回一条消息
        """
        job_node_list = []
        project_id = dag_conf.get("projectId")
        represent_id = dag_conf.get("jobId")
        cat = "job"
        ctype = "node"
        job_name = dag_conf.get("jobDisplayName")
        # name = dag_conf.get("dagName") \
        #        + "_" + dag_conf.get("flowVersion") \
        #        + "_" + dag_conf.get("jobDisplayName") \
        #        + "_" + dag_conf.get("jobVersion")
        level = level_maps["job_level_map"].get(job_name)
        data = {}
        data.update({"table_name": "dag"})
        dag_item = {}
        dag_item.update({"projectId": project_id})
        dag_item.update({"representId": represent_id})
        dag_item.update({"cmessage": job_name})
        dag_item.update({"flowVersion": dag_conf.get("flowVersion")})
        dag_item.update({"sortVersion": dag_conf.get("flowVersion") + "_" + represent_id})
        dag_item.update({"cat": cat})
        dag_item.update({"runtime": dag_conf.get("runtime")})
        dag_item.update({"ctype": ctype})
        dag_item.update({"name": job_name})
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
        job_node_list.append(data)

        return job_node_list

    def determine_node_level(self, dag_conf):

        # 前提 input level 不能大于 output level
        def determine_output_level(dag_conf):
            outputs_level_maps = {}
            outputs = json.loads(dag_conf.get("outputs"))
            for output in outputs:

            # for output_key, output_value in outputs.items():
                projectId = dag_conf.get("projectId")
                get_data = {
                    "table_name": "dag",
                    "key": {
                        "projectId": projectId,
                        "sortVersion": dag_conf.get("flowVersion") + "_" + output.get("id")
                    }
                }
                res = self.dynamodb.getItem(get_data)
                if res.get("Item"):
                    # 如果获取到Item 则说明在dag中有dataset 所以只需要获取level
                    output_level = int(res["Item"].get("level"))
                    if output_level < (-9999):
                        max_level = self.get_max_level("dag", "projectId", dag_conf["projectId"])
                        if max_level < (-9999):
                            output_level = 2
                        else:
                            output_level = max_level + 2
                else:
                    # 如果没有获取到Item 则说明没有dataset 获取 level 最大值 +2
                    max_level = self.get_max_level("dag", "projectId", dag_conf["projectId"])
                    if max_level > (-9999):
                        output_level = max_level + 2
                    else:
                        output_level = 2
                output_level_map = {
                    output.get("id"): output_level
                }
                outputs_level_maps.update(output_level_map)

            return outputs_level_maps

        def determine_job_level(max_input_value):
            job_level = max_input_value + 1
            # name = dag_conf.get("dagName") \
            #        + "_" + dag_conf.get("flowVersion") \
            #        + "_" + dag_conf.get("jobDisplayName") \
            #        + "_" + dag_conf.get("jobVersion")
            name = dag_conf.get("jobDisplayName")
            job_level_map = {
                name: job_level
            }
            return job_level_map

        def determine_input_level(dag_conf):
            # name = dag_conf.get("dagName") \
            #        + "_" + dag_conf.get("flowVersion") \
            #        + "_" + dag_conf.get("jobDisplayName") \
            #        + "_" + dag_conf.get("jobVersion")
            name = dag_conf.get("jobDisplayName")
            inputs_level_maps = {}
            inputs = json.loads(dag_conf.get("inputs"))
            for input in inputs:
            # for input_key, input_value in inputs.items():
                projectId = dag_conf.get("projectId")
                get_data = {
                    "table_name": "dag",
                    "key": {
                        "projectId": projectId,
                        "sortVersion": dag_conf.get("flowVersion") + "_" + input.get("id")
                    }
                }
                res = self.dynamodb.getItem(get_data)
                if res.get("Item"):
                    # 如果获取到Item 则说明在dag中有dataset 所以只需要获取level
                    input_level = int(res["Item"].get("level"))
                    if input_level < (-9999):
                        input_level = 0.1
                else:
                    # 如果没有获取到Item 则说明没有dataset 设置 默认为0
                    input_level = 0.1
                inputs_level_map = {
                    input.get("id"): input_level
                }
                inputs_level_maps.update(inputs_level_map)
            return inputs_level_maps

        def get_max_input_level(inputs_level_maps):
            max_input_level = 0
            for key, value in inputs_level_maps.items():
                if value > max_input_level:
                    max_input_level = value
            if max_input_level == 0.1:
                max_input_level = 0
            return max_input_level

        def process_inputs_level_maps(inputs_level_maps, max_input_value):
            for key, value in inputs_level_maps.items():
                if value == 0.1:
                    inputs_level_maps.update({key: max_input_value})

            return inputs_level_maps

        def judge_level_is_legal(outputs_level_maps, job_level_map):
            for name, output_level in  outputs_level_maps.items():
                if job_level_map.get(dag_conf.get("jobDisplayName")) >= output_level:
                    raise Exception("输入参数level大于输出参数level")

        # 1 确定 output level 如果dag中有，继续使用
        # 如果没有最大 level 加2

        # 2 确定 input level 如果有继续使用
        # 如果第一次创建 并且没有其他input 默认创建level为0
        # 如果有其他已经被使用的input 则第一次使用的和max input level相同

        # 3 确定job node等级 input levels 中 max input level + 1
        outputs_level_maps = determine_output_level(dag_conf)
        inputs_level_maps = determine_input_level(dag_conf)
        max_input_value = get_max_input_level(inputs_level_maps)
        # 把为0的input level处理成 max input level
        process_inputs_level_maps = process_inputs_level_maps(inputs_level_maps, max_input_value)

        job_level_map = determine_job_level(max_input_value)
        # 判断job_level是否大于等于 output level
        judge_level_is_legal(outputs_level_maps, job_level_map)


        level_map = {
            "outputs_level_maps": outputs_level_maps,
            "job_level_map": job_level_map,
            "inputs_level_maps": process_inputs_level_maps
        }
        return level_map

    def create_dataset_data(self, ds, ds_type, level_maps, item, data, dag_conf):
        level_map = level_maps.get(ds_type + "_level_maps")
        level = level_map.get(ds.get("id"))
        item.update({"representId": ds.get("id")})
        item.update({"flowVersion": dag_conf.get("flowVersion")})
        item.update({"sortVersion": dag_conf.get("flowVersion") + "_" + ds.get("id")})
        item.update({"name": ds.get("name")})
        item.update({"level": str(level)})
        data.update({"item": item})
        return data

    def put_dataset_node(self, node_data, item, dag_conf, ds_type, level_maps):
        dataset_node_list = []
        for ds in json.loads(dag_conf.get(ds_type)):
            node_data = self.create_dataset_data(ds, ds_type, level_maps, item, node_data, dag_conf)
            # print("dataset node ===============================================")
            # print(node_data)
            # self.dynamodb.putData(node_data)
        return dataset_node_list

    def create_dataset_node(self, dag_conf, level_maps):
        """
        根据 dag_conf 的列表 分別创建每个dataset 对应的node
        :param dag_conf_list: dag的详细参数的列表
        :return: 创建dataset_node成功后返回一条消息
        """

        data = {}
        item = {}
        data.update({"table_name": "dag"})
        item.update({"projectId": dag_conf.get("projectId")})
        item.update({"cat": "dataset"})
        item.update({"ctype": "node"})
        item.update({"runtime": "intermediate"})
        position = {
            "x": "0",
            "y": "0",
            "z": "0",
            "w": "0",
            "h": "0",
        }
        item.update({"position": json.dumps(position)})
        output_dataset_node_list = self.put_dataset_node(data, item, dag_conf, ds_type="outputs", level_maps=level_maps)
        input_dataset_node_list = self.put_dataset_node(data, item, dag_conf, ds_type="inputs", level_maps=level_maps)
        output_dataset_node_list.extend(input_dataset_node_list)

        return output_dataset_node_list

    def create_node(self, dag_conf, level_maps):
        """
        创建 dag node
        :param dag_conf_list: dag的详细参数的列表
        """
        # 创建dataset的node
        dataset_node_list = self.create_dataset_node(dag_conf, level_maps)
        # 创建job的node
        job_node_list = self.create_job_node(dag_conf, level_maps)

        job_node_list.extend(dataset_node_list)
        return job_node_list

    def create_dag(self, dag_conf):
        """
        创建 dag link
        :param dag_conf_list: dag的详细参数的列表
        """
        level_maps = self.determine_node_level(dag_conf)

        # 根据创建 event 下所有的dag_conf 创建link
        link_list = self.create_link(dag_conf)

        # # 根据dag_conf 和 level_maps 创建dataset
        node_list = self.create_node(dag_conf, level_maps)
        link_list.extend(node_list)

        return link_list

    def exec(self, dag_conf):
        logging.info(dag_conf)
        logging.info("运行创建dag命令")
