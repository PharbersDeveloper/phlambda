import json
import logging

from delegate.project.max import Max
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL

# project_table = {
#     "Test": Max,
#     "Auto_max_refactor": Max,
#     "ETL_Iterator": Max,
#     "Test_Alex": Max,
#     "Auto_Raw_Data": Max,
#     "max": Max,
#     "Auto_rf_factor": Max,
#     "Auto_weight": Max,
#     "Auto_max_check": Max,
#     "Auto_max_delivery": Max,
#     "Auto_cMax": Max,
#     "test_python3": Max
# }

class Execute:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.logger = PhLogging().phLogger("创建流程入口", LOG_DEBUG_LEVEL)
            

    def process_insert_event(self):
        # 获取新插入item的 partition_key, sort_key, message
        item_list = []
        records = self.event.get("Records")
        for record in records:
            if record.get("eventName") == "INSERT":
                self.logger.debug(record.get("eventName"))
                new_image = record["dynamodb"]["NewImage"]
                item = {}
                for item_key in list(new_image.keys()):
                    value = new_image[item_key]
                    item_value = list(value.keys())[0]
                    item[item_key] = value[item_value]

                item_list.append(item)

        item_list = self.screen_regular_item(item_list)
        return item_list

    def screen_regular_item(self, item_list):
        jobCats = ["dag_refresh", "prepare_edit", "dag_create"]
        for item in item_list:
            if item.get("jobCat") in jobCats:
                self.logger.debug("item符合创建job形式")
            else:
                item_list.remove(item)

        return item_list

    def exec(self):
        # 获取所有的item
        item_list = self.process_insert_event()
        if item_list:
            self.logger.debug("item_list生成成功")
            for item in item_list:
                dag_type = item.get("jobCat")
                self.logger.debug(json.loads(item.get("message")).get("projectName"))
                # project_init = project_table[json.loads(item.get("message")).get("projectName")]()
                Max().exec(item, dag_type)
        else:
            self.logger.debug("action不是INSERT")


if __name__ == '__main__':
    with open("../events/event_a.json") as f:
        event = json.load(f)
    app = Execute(event=event)
    app.exec()