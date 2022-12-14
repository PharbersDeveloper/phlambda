import boto3
import json
from util.GenerateID import GenerateID
from util.HandleEvent import HandleEvent, EventTracking
import os

evn_mode = "V2" if str(os.getenv("EDITION")).strip().lower() == "v2" else "dev"
evn_queue_url = f"_{evn_mode}.fifo"
jobcat_queue_urls = {
    "project_file_to_DS": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phxlsxtockhouse"+evn_queue_url,  #ph_lmd_phxlsxtockhouse_V2
    "remove_DS": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phremoveds"+evn_queue_url,    #lmd-phremoveds-V2
    "remove_Job": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phremoveds"+evn_queue_url,   #lmd-phremoveds-V2
    "clear_DS_data": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phcleards"+ evn_queue_url,    #lmd-phcleards-V2
    "transform_schema": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phtransformschema"+evn_queue_url,  #lmd-phtransformschema-V2
    "project_files": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phsyncdyevent"+evn_queue_url,     #lmd-phsyncdyevent-V2
    "resource_create": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_dagresource"+evn_queue_url,   #lmd-dagresource-V2
    "resource_delete": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_dagresource"+evn_queue_url,   #lmd-dagresource-V2
    "dag_refresh": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phsyncdagconf" + evn_queue_url,  #lmd-phsyncdagconf-V2
    "prepare_edit": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phsyncdagconf" + evn_queue_url, #lmd-phsyncdagconf-V2
    "dag_create": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phsyncdagconf" + evn_queue_url,  #lmd-phsyncdagconf-V2
    "edit_sample": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_sample"+evn_queue_url,  #lmd-sample-V2
    "catalog": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phmaxcompatible"+evn_queue_url, #lmd-phmaxcompatible-dev
    "max1.0": "https://sqs.cn-northwest-1.amazonaws.com.cn/444603803904/ph_lmd_phmaxcompatible"+evn_queue_url,  #lmd-phmaxcompatible-dev
}

def handle_sqs_key(input_dict):
    sqs_dict = dict(zip(list(map(lambda x: str(x).lower(), input_dict.keys())), input_dict.values()))
    return sqs_dict
jobcat_queue_urls = handle_sqs_key(jobcat_queue_urls)


class SQS(object):

    def __init__(self, **kwargs):
        self.sqs_client = boto3.client('sqs')

    def handle_jobcat(self, jobcat_name):
        if str(jobcat_name).lower() in list(jobcat_queue_urls.keys()):
            sqs_url = jobcat_queue_urls[str(jobcat_name).lower()]
        else:
            print(f"{jobcat_name} not in jobCat: {list(jobcat_queue_urls.keys())}")
            sqs_url = None
        return jobcat_name, sqs_url

    def sqs_send_message(self, message):

        handle_event = HandleEvent(message)
        jobcat_name, Queue_Url = self.handle_jobcat(handle_event.get_jobCat())
        #--??????jobcat ??????
        try:
            if Queue_Url == None:
                print(f"jobCat: {jobcat_name}, ?????????????????? {Queue_Url} ??????")
            else:
                response = self.sqs_client.send_message(
                    QueueUrl=Queue_Url,
                    MessageBody=json.dumps(message, ensure_ascii=False),
                    MessageGroupId=GenerateID().generate(),
                    MessageDeduplicationId=GenerateID().generate()
                )
                print(f"jobCat: {jobcat_name}, ?????????????????? {Queue_Url} ??????")
                #--????????????
                print("-------->> ????????????")
                EventTracking(message).event_tracking_with_jobcat()
        except Exception as e:
            #print(f"jobCat: {jobcat_name}, ?????????????????? {Queue_Url} ??????")
            print("*"*50 + "????????????" + "*"*50)
            print(str(e))
