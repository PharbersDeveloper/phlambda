import json

from ExecHandler import html


def read_file():
    last_data_list = []
    file = open('data.txt')
    for line in file.readlines():
        data = {}
        line = line.replace("\n", '')
        data_list = line.split(",")
        data["id"] = data_list[0]
        data["title"] = data_list[1].replace(' ', '')
        data["url"] = f'https://s3.cn-northwest-1.amazonaws.com.cn/general.pharbers.com/html/{data_list[0]}.html'
        data["date"] = data_list[2].replace(' ', '')
        last_data_list.append(data)
    print(last_data_list)
    return last_data_list


def lambda_handler(event, context):
    return html(read_file())

