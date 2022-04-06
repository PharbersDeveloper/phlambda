import boto3
import json
from util.GenerateID import GenerateID
import re


_jobcat_queue_urls = {
    "": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph-dsevent-pipeline.fifo",
    "project_file_to_DS": "",
    "remove_DS": "",
    "clear_DS_data": "",
    "transform_schema": "",
    "project_files": "",
    "resource_create": "",
    "resource_delete": "",
    "dag_refresh": "",
    "dag_create": "",
    "edit_sample":"",
}

class SQS():

    def __init__(self, **kwargs):

        self.sqs_client = boto3.client('sqs')

    def handle_jobcat(self, event_dict):
        def search_info(string_line, key):
            patter_rule = f" .({key}).: ..S.: .(.*?).., "
            search_result = re.findall(pattern=patter_rule, string=str(string_line))
            return search_result
        jobcat_name = search_info(event_dict, "jobCat")
        #jobdesc = search_info(event_dict, "jobDesc")
        return jobcat_name, _jobcat_queue_urls[jobcat_name][0][0]

    def sqs_send_message(self, message):
       #--基于jobcat 分发
       try:
            print("发消息到队列...成功")
            jobcat_name, Queue_Url = self.handle_jobcat(message)
            print("message id ========================")
            response = self.sqs_client.send_message(
                QueueUrl=Queue_Url,
                MessageBody=json.dumps(message, ensure_ascii=False),
                MessageGroupId=GenerateID().generate()
            )
       except Exception as e:
           print("发消息到队列...失败")
           print(str(e))
       '''
        # response = self.sqs_client.send_message(
        #     QueueUrl="https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph-dagtrigger-pipeline.fifo",
        #     MessageBody=json.dumps(message, ensure_ascii=False),
        #     MessageGroupId=GenerateID().generate()
        # )
        response = self.sqs_client.send_message(
            QueueUrl="https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph-dsevent-pipeline.fifo",
            MessageBody=json.dumps(message, ensure_ascii=False),
            MessageGroupId=GenerateID().generate()
        )

        print("发送消息到sample")
        response = self.sqs_client.send_message(
            QueueUrl="https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph-sample-pipeline-V2.fifo",
            MessageBody=json.dumps(message, ensure_ascii=False),
            MessageGroupId=GenerateID().generate()
        )

        response = self.sqs_client.send_message(
            QueueUrl="https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph-dyevent-pipeline.fifo",
            MessageBody=json.dumps(message, ensure_ascii=False),
            MessageGroupId=GenerateID().generate()
        )
        '''
