from functools import reduce


class Expression:
    __dynamodb_type = {
        "str": "S",
        "int": "N",
        "float": "N",
    }

    def get_type(self, target):
        return str(type(target)).replace("<class", "").replace("'", "").replace(">", "").replace(" ", "")

    def __build_attr(self, key, value, filter_expr):
        value_type = self.__dynamodb_type.get(self.get_type(value), "str")
        expression_attr_name = {
            f"#{key}": key
        }
        expression_attr_value = {
            f":{key}": {
                f"{value_type}": value
            }
        }
        return {
            "FilterExpression": filter_expr,
            "ExpressionAttributeName": expression_attr_name,
            "ExpressionAttributeValue": expression_attr_value
        }

    # todo 这块还能再优化
    def toValue(self, key, op, value):
        filter_expression = f"#{key} {op} :{key}"
        attr = self.__build_attr(key, value, filter_expression)
        return attr

    def toArray(self, key, op, value):
        exprs = list(map(lambda x: f":{key}{x}", range(len(value))))
        filter_expression = f"#{key} {op} ({', '.join(exprs)})"
        attr = self.__build_attr(key, value, filter_expression)
        expr_values = {}
        for i, item in enumerate(exprs):
            value_type = self.__dynamodb_type.get(self.get_type(value[i]), "str")
            expr_values[item] = {
                f"{value_type}": value[i]
            }
        attr["ExpressionAttributeValue"] = expr_values
        return attr

    def toBeginsWith(self, key, op, value):
        filter_expression = f"{op}({key}, :{key})"
        attr = self.__build_attr(key, value, filter_expression)
        attr["ExpressionAttributeName"] = {}
        return attr

    __structure = {
        "query": "Key",
        "scan": "Attr",
        "=": toValue,
        "in": toArray,
        ">": toValue,
        ">=": toValue,
        "<": toValue,
        "<=": toValue,
        "<>": toValue,
        "begins_with": toBeginsWith,
    }

    def __init__(self):
        pass

    def __assemble(self, data):
        key = data["key"]
        content = data["value"]
        [op, value] = content[key]
        return self.__structure.get(op, "=")(self, key, op, value)

    # 表达式组装
    def join_expr(self, value):
        keys = list(map(lambda key: {
            "key": key,
            "value": value
        }, list(value.keys())))
        exprs = list(map(self.__assemble, keys))
        filter_expression = " AND ".join(list(map(lambda item: item["FilterExpression"], exprs)))
        expression_attr_names = {}
        expression_attr_values = {}
        for item in exprs:
            expression_attr_names = dict(expression_attr_names, **item["ExpressionAttributeName"])

        for item in exprs:
            expression_attr_values = dict(expression_attr_values, **item["ExpressionAttributeValue"])

        return {
            "FilterExpression": filter_expression,
            "ExpressionAttributeNames": expression_attr_names,
            "ExpressionAttributeValues": expression_attr_values
        }

    # 非表达式组装
    def assemble_batch_item_keys(self, value):
        keys = []
        for item in value:
            temp = {}
            for key in list(item.keys()):
                value_type = self.__dynamodb_type.get(self.get_type(item[key]), "str")
                temp[key] = {
                    f"{value_type}": item[key]
                }
            keys.append(temp)
        return keys
