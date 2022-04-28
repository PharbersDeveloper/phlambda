import json


class Check:

    ds_sc = False

    def checkdata(self, data_list, value):
        if not isinstance(data_list, list):
            raise
        for data in data_list:
            if not set(value) <= set(list(data.keys())):
                raise
            self.ds_sc = True

    def checktype(self, data):
        if data:
            inputs = json.loads(data.get('inputs'))
            output = json.loads(data.get('output'))
            if not isinstance(inputs, list) or not isinstance(output, dict):
                raise

    def check_parameter(self, data):
        try:
            ds_value = ['cat', 'format', 'name', ]
            script_value = ["name", "flowVersion", "inputs", "output"]

            # 1. common 必须存在
            if not data.get("common"):
                raise

            # 2. action 必须存在
            if not data.get("action"):
                raise

            # 3. notification 必须存在
            if not data.get("notification"):
                raise

            # 4. datasets 和 scripts 必须存在一个

            self.checkdata(data.get("datasets", []), ds_value)
            self.checkdata(data.get("scripts", []), script_value)
            self.checktype(data.get("scripts", []))

            if not self.ds_sc:
                raise
            return True

        except Exception as e:
            print(e)
            return False


def lambda_handler(event, context):
    return Check().check_parameter(event)

    # 1. common 必须存在
    # 2. action 必须存在
    # 3. notification 必须存在
    # 4. datasets 和 scripts 必须存在一个
    #   4.1 如果dataset存在，name, cat, format 都必须存在，并判断类型
    #   4.2 如果scripts存在，name, flowVersion, input, output 都必须存在，并判断类型
    # return true
