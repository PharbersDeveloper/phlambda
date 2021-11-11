from boto3.dynamodb.conditions import Key, Attr


class Expression:
    structure = {
        "query": "Key",
        "scan": "Attr"
    }

    def __init__(self):
        pass

    def join_expr(self, type, value):
        pattern_cond = self.structure.get(type)

        expr_str = "&".join(list(map(
            lambda key: """{}("{}").{}("{}")""".format(pattern_cond, key, "eq", value.get(key)),
            list(value.keys()))))
        return eval(expr_str)
