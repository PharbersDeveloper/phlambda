import os, sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
import boto3

client = boto3.client('s3')
os_env = os.environ
os_env['USER'] = 'mesong@data-pharbers.com'
os_env['KEY'] = '{"Bucket": "ph-platform", "Key": "2020-11-11/template/email/email-forgetpwd.html"}'
os_env['PSWD'] = 'song19980825'
os_env['HOST'] = 'smtp.ym.163.com'
os_env['PORT'] = '465'
os_env['SENDER'] = 'mesong@data-pharbers.com'
os_env['SENDER_NAME'] = "法伯科技"

user = os.getenv("PH_EMAIL_USER", os_env['USER'])
pswd = os.getenv("PH_EMAIL_PSWD", os_env['PSWD'])
host = os.getenv("PH_EMAIL_SERVER_HOST", os_env['HOST'])
port = os.getenv("PH_EMAIL_SERVER_PORT", os_env['PORT'])
key = json.loads(os_env['KEY'])


def send_email(addressees, subject, content, attach_files=None, content_type='plain',
               sender_name=os_env['SENDER_NAME']):
    for addressee in addressees:
        msg = MIMEMultipart()
        msg['From'] = Header(sender_name, 'utf-8')
        msg['To'] = Header(addressee['addresses_name'])
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
        server.sendmail(os_env["SENDER"], addressee['addresses'], msg.as_string())
        server.quit


def s3Read(key):
    response = client.get_object(
        Bucket=key['Bucket'],
        Key=key['Key'],
    )
    content = response['Body'].read().decode()
    return content


def lambdaHandler(event, context):
    subject = "修改密码"
    content_type = "html"
    content = s3Read(key)
    if event['type'] == "forget_password":
        addressees = [
            {"addresses_name": event["email"], "addresses": event["email"]},
        ]
        send_email(
            addressees=addressees,
            subject=subject,
            content=content,
            content_type=content_type
        )
        return {
            "statusCode": 200,
            "body": json.dumps("repassword success")
        }
    elif event['type'] == "test":
        addressees = [
            {"addresses_name": event["email"], "addresses": event["email"]},
        ]
        content = "测试案例"
        attach_files = [
            {"file_name": "test1.yaml",
             "file_context": ['PH_NOTICE_EMAIL:\n', '  metadata:\n', '    name: PH_NOTICE_EMAIL\n']},
            {"file_name": "test2.txt", "file_context": ["xxxxxxxxxxxxxxxxxx"]},
            # {"file_name": "test3.png", "file_context" : ["xxxxxxxxxxxxxxxxxx"]}
        ]
        send_email(
            addressees=addressees,
            subject=subject,
            content=content,
            content_type=content_type,
            attach_files=attach_files
        )
        return {
            "statusCode": 200,
            "body": json.dumps("test_success")
        }

