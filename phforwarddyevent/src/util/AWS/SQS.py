import boto3
import json
from util.GenerateID import GenerateID
from phmetrixlayer import aws_cloudwatch_put_metric_data

jobcat_queue_urls = {
    "project_file_to_DS": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phxlsxtockhouse_V2.fifo",  #ph_lmd_phxlsxtockhouse_V2
    "remove_DS": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phremoveds_V2.fifo",    #lmd-phremoveds-V2
    "remove_Job": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phremoveds_V2.fifo",   #lmd-phremoveds-V2
    "clear_DS_data": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phcleards_V2.fifo",       #lmd-phcleards-V2
    "transform_schema": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phtransformschema_V2.fifo",   #lmd-phtransformschema-V2
    "project_files": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phsyncdyevent_V2.fifo",     #lmd-phsyncdyevent-V2
    "resource_create": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_dagresource_V2.fifo",   #lmd-dagresource-V2
    "resource_delete": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_dagresource_V2.fifo",   #lmd-dagresource-V2
    "dag_refresh": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phsyncdagconf_V2.fifo",      #lmd-phsyncdagconf-V2
    "prepare_edit": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phsyncdagconf_V2.fifo",      #lmd-phsyncdagconf-V2
    "dag_create": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phsyncdagconf_V2.fifo",       #lmd-phsyncdagconf-V2
    "edit_sample": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_sample_V2.fifo", #lmd-sample-V2
}

def handle_sqs_key(input_dict):
    sqs_dict = dict(zip(list(map(lambda x: str(x).lower(), input_dict.keys())), input_dict.values()))
    return sqs_dict
jobcat_queue_urls = handle_sqs_key(jobcat_queue_urls)

class SQS(object):

    def __init__(self, **kwargs):
        self.sqs_client = boto3.client('sqs')

    def handle_jobcat(self, event):
        dynamodb_data, message_data = self.parse_event_parameters(event)
        jobcat_name = dynamodb_data['jobCat']['S']
        if str(jobcat_name).lower() in list(jobcat_queue_urls.keys()):
            sqs_url = jobcat_queue_urls[str(jobcat_name).lower()]
        else:
            print(f"{jobcat_name} not in jobCat: {list(jobcat_queue_urls.keys())}")
            sqs_url = None
        return jobcat_name, sqs_url

    def parse_event_parameters(self, event):
        body_data = eval(event['Records'][0]['body'])
        dynamodb = body_data['Records'][0]['dynamodb']
        dynamodb_data = dynamodb['NewImage']
        message_data = eval(dynamodb_data['message']['S'])
        return dynamodb_data, message_data

    #--埋点
    def event_tracking(self, event):
        dynamodb_data, message_data = self.parse_event_parameters(event)
        project_id = dynamodb_data['projectId']['S']
        project_name = message_data['project_name']
        current_user_id = message_data['conf']['ownerId']
        current_name = dynamodb_data['owner']['S']
        action_mode = dynamodb_data['jobCat']['S']
        #action_detail = dynamodb_data['jobDesc']['S']
        action_detail = message_data['conf']['jobDesc']

        return aws_cloudwatch_put_metric_data(project_id,
                                       project_name,
                                       current_user_id,
                                       current_name,
                                       action_mode,
                                       action_detail)

    def sqs_send_message(self, message):

       #--基于jobcat 分发
        try:
            jobcat_name, Queue_Url = self.handle_jobcat(message)
            if Queue_Url == None:
                print(f"jobCat: {jobcat_name}, 发消息到队列 {Queue_Url} 失败")
            else:
                response = self.sqs_client.send_message(
                    QueueUrl=Queue_Url,
                    MessageBody=json.dumps(message, ensure_ascii=False),
                    MessageGroupId=GenerateID().generate(),
                    MessageDeduplicationId=GenerateID().generate()
                )
                print(f"jobCat: {jobcat_name}, 发消息到队列 {Queue_Url} 成功")
                print("*"*50 + "event tracking" + "*"*50)
                self.event_tracking(message)
        except Exception as e:
            #print(f"jobCat: {jobcat_name}, 发消息到队列{Queue_Url}失败")
            print("*"*50 + "错误信息" + "*"*50)
            print(str(e))