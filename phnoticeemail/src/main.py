import os, sys
import logging
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders

phlogger = logging.getLogger("ph-log")
formatter = logging.Formatter("{ 'Time': %(asctime)s, 'Message': %(message)s, 'File': %(filename)s, 'Func': "
                                      "%(funcName)s, 'Line': %(lineno)s, 'Level': %(levelname)s } ")
sys_handler = logging.StreamHandler(stream=sys.stdout)
sys_handler.setFormatter(formatter)
phlogger.addHandler(sys_handler)
phlogger.setLevel(logging.DEBUG)

DEFAULT_USER = 'project@data-pharbers.com'
DEFAULT_PSWD = 'qiye@126'
DEFAULT_HOST = 'smtp.ym.163.com'
DEFAULT_PORT = 465
DEFAULT_SENDER = 'project@data-pharbers.com'
DEFAULT_SENDER_NAME = "法伯科技"

user = os.getenv("PH_EMAIL_USER", DEFAULT_USER)
pswd = os.getenv("PH_EMAIL_PSWD", DEFAULT_PSWD)
host = os.getenv("PH_EMAIL_SERVER_HOST", DEFAULT_HOST)
port = os.getenv("PH_EMAIL_SERVER_PORT", DEFAULT_PORT)

def send_email(addressees, subject, content, attach_files=None, content_type='plain', sender_name=DEFAULT_SENDER_NAME):
    # version2
    for addressee in addressees:
        
        msg = MIMEMultipart()
        msg['From'] = Header(sender_name, 'utf-8')
        msg['To'] = Header(addressee['addressee_name'])
        msg['Subject'] = Header(subject)
        msg.attach(MIMEText(content, content_type, 'utf-8'))

        if attach_files is not None:
            for attach_file in attach_files:
                if attach_file['file_name'].endswith('png'):
                    # 设置附件的MIME和文件名，这里是png类型:
                    att = MIMEBase('image', 'png', filename=attach_file['file_name'])
                    # 加上必要的头信息:
                    att.add_header('Content-Disposition', 'attachment', filename=attach_file['file_name'])
                    att.add_header('Content-ID', '<0>')
                    att.add_header('X-Attachment-Id', '0')
                    # 把附件的内容读进来:
                    att.set_payload(attach_file['file_context'])
                    # 用Base64编码:
                    encoders.encode_base64(att)
                    msg.attach(att)
                else:
                    att = MIMEText("".join(attach_file['file_context']), 'base64')
                    att["Content-Type"] = 'application/octet-stream'
                    att["Content-Disposition"] = "'attachment; filename=" + attach_file['file_name'] + " '"
                    msg.attach(att)

        server = smtplib.SMTP_SSL(host, port)
        server.login(user, pswd)
        server.sendmail(DEFAULT_SENDER, addressee['addressee'], msg.as_string())
        server.quit

def lambda_handler(event, context):
    '''
    event content: 
        {   
            "attach_files" : [
                {"file_name" : "test1.txt", "file_context" : ["xxxxxxxxxxxxxxxxxx"]},
                {"file_name" : "test2.txt", "file_context" : ["xxxxxxxxxxxxxxxxxx"]}
            ]
            "addressees": [
                {"addressee_name" : "qq_addressee", "addressee":"1340798171@qq.com"},
                {"addressee_name" : "163_addressee", "addressee":"15847059648@163.com"},
            ],
            "subject": "邮件主题",
            "content_type": "text/plain",
            "content": "邮件发送内容",
            "sender_name": "发件人名称"
        }
    '''
    phlogger.info("event = " + str(event))

    if 'Records' in event:
        records = event['Records'][0]
        if 'EventSource' in records and records['EventSource'] == 'aws:sns':
            message = records['Sns']['Message']
            event = json.loads(message)
    phlogger.info("actual_event = " + str(event))
    
    addressees = event['addressees']
    subject = event['subject']
    content = event['content'] 
    content_type = event.get("content_type", "plain")
    sender_name = event.get("sender_name", DEFAULT_SENDER_NAME)
    attach_files = event.get("attach_files", None)
    
    send_email(
        addressees=addressees,
        subject=subject,
        content=content,
        content_type=content_type,
        sender_name=sender_name,
        attach_files=attach_files
    )

if __name__ == '__main__':
    # 测试 cicd中merge代码 打印下merge的参数1948
    phlogger.info("__main__")
    
    addressees = [
        {"addressee_name" : "qq_addressee", "addressee":"1340798171@qq.com"},
        {"addressee_name" : "163_addressee", "addressee":"15847059648@163.com"},
    ]
    attach_files = [
        {"file_name" : "test1.yaml", "file_context" : ['PH_NOTICE_EMAIL:\n', '  metadata:\n', '    name: PH_NOTICE_EMAIL\n']},
        {"file_name" : "test2.txt", "file_context" : ["xxxxxxxxxxxxxxxxxx"]},
        # {"file_name" : "test3.png", "file_context" : ["xxxxxxxxxxxxxxxxxx"]}
    ]
    subject = "邮件主题"
    content = """
        邮件发送
    <p>Python 邮件发送测试...</p>
    <p><a href="http://www.baidu.com">百度链接</a></p>
    """
    content_type = "html"
    sender_name = None
    
    send_email(
        addressees=addressees,
        subject=subject,
        content=content,
        attach_files=attach_files,
        content_type = content_type
    )