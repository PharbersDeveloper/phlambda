import os, sys
import logging
import json

from deleteCfn import DeleteCfn


def execute(project_name, operate_type):

    DeleteCfn(project_name=project_name).execute()


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


def lambda_handler(self):
    # 获取所有的item
    item_list = self.process_insert_event()
    if item_list:
        for item in item_list:
            backup_status = item.get("backup_status")
            project_name = item.get("projectName")
            if backup_status == 1:
                execute(project_name)

    else:
        print("action不是INSERT")