import os, sys
import json
import logging

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


DEFAULT_SMS_ACCESS_KEY = "LTAI4GBmeNMAyiYyjHzP1a4p"
DEFAULT_SMS_SECRET_KEY = "X7ilgJDT8sgxxB5gwOGKwz8wZ9ybUl"
DEFAULT_SMS_REGION = "cn-hangzhou"


phlogger = logging.getLogger("ph-log")
formatter = logging.Formatter("{ 'Time': %(asctime)s, 'Message': %(message)s, 'File': %(filename)s, 'Func': "
                                      "%(funcName)s, 'Line': %(lineno)s, 'Level': %(levelname)s } ")
sys_handler = logging.StreamHandler(stream=sys.stdout)
sys_handler.setFormatter(formatter)
phlogger.addHandler(sys_handler)
phlogger.setLevel(logging.DEBUG)


def send_sms(phone_number, sign_ame, tmpl_code, tmpl_param):
    client = AcsClient(
        os.getenv("SMS_ACCESS_KEY", DEFAULT_SMS_ACCESS_KEY),
        os.getenv("SMS_SECRET_KEY", DEFAULT_SMS_SECRET_KEY),
        os.getenv("SMS_REGION", DEFAULT_SMS_REGION),
    )

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', os.getenv("SMS_REGION", DEFAULT_SMS_REGION))
    request.add_query_param('PhoneNumbers', phone_number)
    request.add_query_param('SignName', sign_ame)
    request.add_query_param('TemplateCode', tmpl_code)
    request.add_query_param('TemplateParam', tmpl_param)

    response = client.do_action(request)
    return str(response, encoding = 'utf-8')


def lambda_handler(event, context):
    '''
    event content: 
        {
            "phone_number": "17643233157",
            "sign_ame": "法伯科技",
            "tmpl_code": "SMS_117415068", # 模板 ID，需要新或查看所有的模板，需要登录 aliyun 
            "tmpl_param": {"code": 123456} # 基于模板传递的指定参数
        }
    '''
    phlogger.info("event = " + str(event))

    if 'Records' in event:
        records = event['Records'][0]
        if 'EventSource' in records and records['EventSource'] == 'aws:sns':
            message = records['Sns']['Message']
            event = json.loads(message)
    phlogger.info("actual_event = " + str(event))

    phone_number = event['phone_number']
    sign_ame = event['sign_ame']
    tmpl_code = event['tmpl_code']
    tmpl_param = event['tmpl_param']

    response = send_sms(
        phone_number = phone_number, 
        sign_ame = sign_ame, 
        tmpl_code = tmpl_code, 
        tmpl_param = tmpl_param
    )

    return { 
        'message': 'SMS send {sign_ame}、{tmpl_code}、{tmpl_param} to phone_number={phone_number}'.format(
            sign_ame=sign_ame, 
            tmpl_code=tmpl_code, 
            tmpl_param=tmpl_param, 
            phone_number=phone_number,
        ),
        'response': response
    }


if __name__ == '__main__':
    phlogger.info("__main__")
    
    phone_number = "17643233157",
    sign_ame = "法伯科技",
    tmpl_code = "SMS_117415068",
    tmpl_param = {"code": 123456}
    
    response = send_sms(
        phone_number = phone_number, 
        sign_ame = "法伯科技", 
        tmpl_code = "SMS_117415068", 
        tmpl_param = {"code": 123456}
    )
    
    print('SMS send {sign_ame}、{tmpl_code}、{tmpl_param} to phone_number={phone_number}, response={response}'.format(
            sign_ame=sign_ame, 
            tmpl_code=tmpl_code, 
            tmpl_param=tmpl_param, 
            phone_number=phone_number,
            response=response,
        )
    )

spark-submit --master yarn --deploy-mode cluster 
--name autodatamatchnewcodetestdatamatchingcleaningdatanormalization-f 
--proxy-user airflow --queue airflow 
--conf spark.driver.cores=1 --conf spark.driver.memory=3g 
--conf spark.executor.cores=4 --conf spark.executor.memory=2g 
--conf spark.executor.instances=4 --conf spark.driver.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Dcom.amazonaws.services.s3.enableV4 
--conf spark.executor.extraJavaOptions=-Dfile.encoding=UTF-8 -Dsun.jnu.encoding=UTF-8 -Dcom.amazonaws.services.s3.enableV4 
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem 
--conf spark.hadoop.fs.s3a.access.key=AKIAWPBDTVEANRUMG5P6 
--conf spark.hadoop.fs.s3a.secret.key=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 
--conf spark.hadoop.fs.s3a.endpoint=s3.cn-northwest-1.amazonaws.com.cn 
--conf jars=s3a://ph-platform/2020-11-11/jobs/python/phcli/common/aws-java-sdk-bundle-1.11.828.jar,s3a://ph-platform/2020-11-11/jobs/python/phcli/common/hadoop-aws-3.2.1.jar 
--conf spark.sql.codegen.wholeStage=False 
--conf spark.sql.execution.arrow.pyspark.enable=true 
--conf spark.sql.crossJoin.enabled=true 
--conf spark.sql.autoBroadcastJoinThreshold=-1 
--conf spark.sql.files.maxRecordsPerFile=554432 
--py-files s3://ph-platform/2020-11-11/jobs/python/phcli/common/phcli-2.2.1-py3.8.egg,s3://ph-test-emr/phjob.py
s3://ph-platform/2020-11-11/jobs/python/phcli/Auto_data_match_newcode_test/data_matching_cleaning_data_normalization/phmain.py

--owner mzhang --run_id manual__testyear-04-08T00_47_13.535678+00_00 --job_id testdatamatchnewcodetestdatamatchingcleaningdatanormalization-f --job_name cleaning_data_normalization --path_prefix s3://ph-max-auto/2020-08-11/data_matching/refactor/runs --path_cleaning_data s3://ph-max-auto/2020-08-11/data_matching/refactor/data/CHC/* --path_human_interfere s3://ph-max-auto/2020-08-11/data_matching/refactor/data/HUMAN_INTERFERE --path_second_human_interfere s3://ph-max-auto/2020-08-11/data_matching/refactor/data/DF_CONF/0.3 --source_data_type chc --cleaning_result cleaning_result --cleaning_origin cleaning_origin

s3://ph-platform/2020-11-11/emr/logs/j-3PJB5MKIEWGSM/steps/s-3EI05MQ8RM7V9/