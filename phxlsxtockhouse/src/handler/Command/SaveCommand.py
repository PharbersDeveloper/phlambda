import json
from handler.Command.Command import Command


class SaveDagCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        self.receiver.save(data)


class SaveDataSetCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        parameters = {
            "ds_id": data["ds_id"],
            "project_id": data["project_id"],
            "name": data["ds_name"],
            "schema": data["standard_schema"],
            "label": data["label"],
            "version": data["version"]
        }

        self.receiver.save(parameters)


class SaveActionCommand(Command):

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self, data):
        parameter = dict({}, **data)
        parameter["message"] = json.dumps(parameter["message"], ensure_ascii=False)
        self.receiver.save(parameter)
