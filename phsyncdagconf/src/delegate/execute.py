import json
import logging

from delegate.project.max import Max


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )

project_table = {
    "max": Max
}

class Execute:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def process_insert_event(self):
        # 获取新插入item的 partition_key, sort_key, message
        item_list = []
        records = self.event.get("Records")
        for record in records:
            if record.get("eventName") == "INSERT":
                logging.info(record.get("eventName"))
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
        for item in item_list:
            if item.get("jobCat"):
                logging.info("item符合创建job形式")
            else:
                item_list.remove(item)

        return item_list

    def exec(self):
        # 获取所有的item
        item_list = self.process_insert_event()
        if item_list:
            logging.info("item_list生成成功")
            for item in item_list:
                dag_type = item.get("jobCat")
                logging.info(json.loads(item.get("message")).get("projectName"))
                project_init = project_table[json.loads(item.get("message")).get("projectName")]()
                project_init.exec(item, dag_type)
        else:
            logging.info("action不是INSERT")


if __name__ == '__main__':
    with open("../events/event_refresh.json") as f:
        event = json.load(f)
    app = Execute(event=event)
    app.exec()