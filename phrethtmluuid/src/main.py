import json

from ExecHandler import html


def read_file():
    data = {}
    file = open('data.txt')
    for line in file.readlines():
        line = line.replace("\n", '')
        data_list = line.split(",")
        data[data_list[0]] = data_list[1]
    return {"data": data}


def lambda_handler(event, context):
    print(json.dumps(html(read_file())))
    return json.dumps(html(read_file()))
