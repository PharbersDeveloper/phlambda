import json
import operator

from util.AWS.DynamoDB import DynamoDB
from delegate.levelTreeNode import LevelTreeNode
from util.GenerateID import GenerateID
from util.AWS import define_value as dv

class DagLevel:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.dynamodb = DynamoDB()

    def update_child_node(self, dag_conf_list, node, root):

        all_node_list = []
        def get_dataset_child():
            dataset_child_node_list = []
            for dag_conf in dag_conf_list:
                if json.dumps(node, ensure_ascii=False) in dag_conf.get("outputs"):
                    child_node = {
                        "jobName": dag_conf.get("jobShowName"),
                        "jobId": dag_conf.get("jobId")
                    }
                    dataset_child_node_list.append(child_node)
            return dataset_child_node_list

        def get_job_child(jobId):
            job_child_node_list = []
            for dag_conf in dag_conf_list:
                if jobId in dag_conf.get("jobId"):
                    job_child_node = eval(dag_conf.get("inputs"))
                    job_child_node_list.extend(job_child_node)
            return job_child_node_list

        if node.get("name"):
            node_type = "dataset"
            child_node_list = get_dataset_child()
            for child_node in child_node_list:
                child = root.add_child(json.dumps(child_node, ensure_ascii=False))
                self.update_child_node(dag_conf_list, child_node, child)
        elif node.get("jobName"):
            node_type = "job"
            child_node_list = get_job_child(node.get("jobId"))
            for child_node in child_node_list:
                child = root.add_child(json.dumps(child_node, ensure_ascii=False))
                self.update_child_node(dag_conf_list, child_node, child)

        all_node_list.extend(child_node_list)
        return all_node_list

    def get_latest_child(self, root_obj=None, max_level=-99999):
        if str(root_obj.items()) == "dict_items([])":
            line = root_obj.path.split("->")
            root_level = len(line) - 1
            if root_level > max_level:
                max_level = root_level
        for name, obj in root_obj.items():
            max_level = self.get_latest_child(obj, max_level)

        return max_level

    def get_child_node_name(self, obj, level, level_map):
        level = level - 1
        for name, child_obj in obj.items():
            dag = eval(name)
            dag["level"] = level
            level_map.append(dag)
            self.get_child_node_name(child_obj, level, level_map)

        return level_map
    def exec(self):

        # 获取当前event的dag_conf_list
        # 判断所有root节点
        root_node_list = [eval(root_dag_conf.get("outputs"))[0] for root_dag_conf in self.dag_conf_list if len(eval(root_dag_conf.get("targetJobId"))) == 0]
        all_node_level_list = []
        for root_node in root_node_list:

            # 创建root_node
            root = LevelTreeNode(json.dumps(root_node, ensure_ascii=False))

            self.update_child_node(self.dag_conf_list, root_node, root)
            # root.dump()
            max_level = self.get_latest_child(root)

            max_dag = eval(root.path)
            max_dag["level"] = max_level
            level_map = []
            level_map.append(max_dag)
            # 从tree读取所有node 并且附加level
            dag_map_list = self.get_child_node_name(root, max_level, level_map)
            all_node_level_list.extend(dag_map_list)

        process_dag = []
        # remove_duplicate_node
        for current_level in all_node_level_list:
            current_id = current_level.get("id")
            if current_id:
                for compare_level in all_node_level_list:
                    if current_id == compare_level.get("id") and not operator.eq(current_level, compare_level):
                        if current_level.get("level") > compare_level.get("level"):
                            current_level = compare_level

            process_dag.append(json.dumps(current_level, ensure_ascii=False))


        return list(set(process_dag))

