import os, sys
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
