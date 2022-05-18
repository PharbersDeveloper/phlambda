import json
import requests
from phResource.command import Command
from util.AWS.DynamoDB import DynamoDB
from util.AWS.SNS import SNS


class CommandStoreCH(Command):

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dynamodb = DynamoDB()
        self.sns = SNS()

    def show_tables(self, target_ip):
        try:
            url = "http://"+ target_ip +":8123/ch/"
            params = {
                "query": "show databases"
            }

            res = requests.post(url=url, params=params)
            if res:
                print("连接成功")
                print(res.text)
                flag = 1
            else:
                print("连接未成功")
                print(res.text)
                flag = 0
        except Exception as e:
            print(e)
            print("连接未成功")
            flag = 0
        finally:
            return flag

    def execute(self):
        # 创建 target group
        # 192.168.16.119

        while 1:
            flag = self.show_tables(self.target_ip)
            if flag == 1:
                print("连接完成 退出循环")
                break
        # 根据ip 连接clickhouse 先判断数据库是否创建完成 再去调用恢复数据lmd
        # 创建完成后通过sns调用恢复数据lmd

        topic_arn = "arn:aws-cn:lambda:cn-northwest-1:444603803904:function:lmd-phclickhouse-glue-dev"
        message = {
            "project_ip": self.target_ip
        }
        self.sns.sns_publish(topic_arn, json.dumps(message, ensure_ascii=False))


