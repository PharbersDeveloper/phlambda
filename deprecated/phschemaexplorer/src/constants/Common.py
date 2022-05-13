import json

PATH_PREFIX = "PATH_PREFIX"

HEADERS = {
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
}


def serialization(data, code=200):
    content = {
        "headers": HEADERS,
        "statusCode": code,
    }
    if isinstance(data, Exception):
        content["body"] = json.dumps({
            "code": data.code,
            "message": data.message
        }, ensure_ascii=False)
    else:
        content["body"] = json.dumps(data, ensure_ascii=False)
    return content


def class_to_dict(obj):
    # 把对象(支持单个对象、list、set)转换成字典
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            # 把Object对象转换成Dict对象
            dict_obj = {}
            dict_obj.update(o.__dict__)
            obj_arr.append(dict_obj)
        return obj_arr
    else:
        dict_obj = {}
        dict_obj.update(obj.__dict__)
        return dict_obj
