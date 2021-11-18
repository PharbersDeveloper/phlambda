import os
import json
from util.AWS.DynamoDB import DynamoDB
from util.GenerateID import GenerateID

class AppLambdaDelegate:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()
        # self.__partition_key = os.getenv("PARTITION_KEY")
        # self.__sort_key = os.getenv("SORT_KEY")

        # import base64
        # from util.AWS.STS import STS
        # from constants.Common import Common
        # sts = STS().assume_role(
        #     base64.b64decode(Common.ASSUME_ROLE_ARN).decode(),
        #     "Ph-Back-RW"
        # )
        # self.dynamodb = DynamoDB(sts=sts)

    def size_format(self, size):
        return '%.0f' % round(float(size/1024))

    def process_insert_event(self):
        # 获取新插入item的 partition_key, sort_key, message
        item_list = []
        records = self.event.get("Records")
        for record in records:
            if record.get("eventName") == "INSERT":
                new_image = record["dynamodb"]["NewImage"]
                item = {}
                for item_key in list(new_image.keys()):
                    value = new_image[item_key]
                    item_value = list(value.keys())[0]
                    item[item_key] = value[item_value]
                item_list.append(item)
        return item_list

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
            self.dynamodb.putData(data)
            dag_conf_list.append(dag_conf)
        return dag_conf_list

    def create_job_node(self, dag_conf_list):
        for dag_conf in dag_conf_list:
            project_id = dag_conf.get("project_id")
            represent_id = dag_conf.get("job_id")
            cat = "job"
            ctype = "node"
            name = dag_conf.get("dag_name") \
                   + "_" + dag_conf.get("flow_version") \
                   + "_" + dag_conf.get("job_name") \
                   + "_" + dag_conf.get("job_version")
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
            self.dynamodb.putData(data)

    def get_represent_id(self, dag_conf):
        def get_input_dateset_id(inputs):
            return [inputs.get(key) for key in inputs.keys()]

        def get_output_dateset_id(outputs):
            return [outputs.get(key) for key in outputs.keys()]

        source_id = get_input_dateset_id(dag_conf.get("inputs"))
        target_id = get_output_dateset_id(dag_conf.get("outputs"))

        return {
            "source_ids": source_id,
            "target_ids": target_id
        }

    def create_dataset_node(self, dag_conf_list):

        def create_input_dataset_node(data, item, dag_conf):
            for key, value in dag_conf.get("inputs").items():
                item.update({"representId": value})
                item.update({"name": key})
                item.update({"level": "1"})
                data.update({"item": item})
                self.dynamodb.putData(data)
                print(data)

        def create_output_dataset_node(data, item, dag_conf):
            for key, value in dag_conf.get("outputs").items():
                item.update({"representId": value})
                item.update({"name": key})
                item.update({"level": "3"})
                data.update({"item": item})
                self.dynamodb.putData(data)
                print(data)

        for dag_conf in dag_conf_list:
            data = {}
            item = {}
            data.update({"table_name": "dag"})
            item.update({"projectId": dag_conf.get("project_id")})
            item.update({"cat": "dataset"})
            item.update({"ctype": "node"})
            item.update({"position": "(0,0)"})
            create_input_dataset_node(data, item, dag_conf)
            create_output_dataset_node(data, item, dag_conf)


        return ""

    def create_link(self, dag_conf):

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
                self.dynamodb.putData(data)


        def create_source_target_map(represent_ids):
            job_id = dag_conf.get("job_id")
            id_maps = []
            for key, value in represent_ids.items():
                if key == "source_ids":
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
            represent_ids = self.get_represent_id(dag_conf)
            messages = create_source_target_map(represent_ids)
            put_link_to_database(messages)

    def create_node(self, dag_conf_list):

        # 创建dataset的node
        self.create_dataset_node(dag_conf_list)
        # 创建job的node
        self.create_job_node(dag_conf_list)

    def create_dag(self, dag_conf_list):

        # 根据创建 event 下所有的dag_conf 创建link
        self.create_link(dag_conf_list)

        self.create_node(dag_conf_list)


    def exec(self):

        item_list = app.process_insert_event()
        dag_conf_list = self.insert_dagconf(item_list)
        self.create_dag(dag_conf_list)


if __name__ == '__main__':
    with open("../events/event.json") as f:
        event = json.load(f)
    app = AppLambdaDelegate(event=event)
    item_list = app.process_insert_event()
    dag_conf_list = app.insert_dagconf(item_list)
    print(dag_conf_list)
    # app.create_dag(dag_conf_list)