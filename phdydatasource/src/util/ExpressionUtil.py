from boto3.dynamodb.conditions import Key, Attr


class Expression:
    structure = {
        "query": "Key",
        "scan": "Attr",
        "=": "eq",
        "in": "is_in",
        ">": "gt",
        ">=": "gte",
        "<": "lt",
        "<=": "lte",
        "!=": "ne",
        "begins_with": "begins_with",
    }

    # todo 这块还能再优化
    def toString(self, key, pattern, op, value):
        result = """{}("{}").{}("{}")""".format(pattern, key, self.structure.get(op, "="), value)
        return result

    def toArray(self, key, pattern, op, value):
        result = """{}("{}").{}({})""".format(pattern, key, self.structure.get(op, "="), value)
        return result

    def toInt(self, key, pattern, op, value):
        result = """{}("{}").{}({})""".format(pattern, key, self.structure.get(op, "="), value)
        return result

    def toDouble(self, key, pattern, op, value):
        result = """{}("{}").{}({})""".format(pattern, key, self.structure.get(op, "="), value)
        return result

    __convert_data = {
        "str": toString,
        "list": toArray,
        "int": toInt,
        "float": toDouble,
    }

    def __init__(self):
        pass

    def __assemble(self, data):
        key = data["key"]
        pattern = data["pattern"]
        content = data["value"]
        [op, value] = content[key]
        # todo 不太想写正则 后续改吧
        category = str(type(value)).replace("<class", "").replace("'", "").replace(">", "").replace(" ", "")
        return self.__convert_data.get(category, "str")(self, key, pattern, op, value)

    # 表达式组装
    def join_expr(self, types, value):
        pattern_cond = self.structure.get(types)
        keys = list(map(lambda key: {
            "key": key,
            "pattern": pattern_cond,
            "value": value
        }, list(value.keys())))
        expr_str = "&".join(list(map(self.__assemble, keys)))
        print(expr_str)
        return eval(expr_str)

    # 非表达式组装, todo 目前只支持string
    def assemble_batch_item_keys(self, value):
        keys = []
        for item in value:
            temp = {}
            for key in list(item.keys()):
                temp[key] = {
                    "S": item[key]
                }
            keys.append(temp)
        return keys

