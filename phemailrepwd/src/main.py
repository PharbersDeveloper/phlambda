import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
import boto3

os_env = os.environ


def sendEmail(addresses, subject, content, attach_files=None, content_type='plain',
              sender_name=os_env['SENDER_NAME']):
    status = "修改密码的网址发送成功"
    msg = MIMEMultipart()
    msg['From'] = Header(sender_name, 'utf-8')
    msg['To'] = Header(addresses)
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
                status = "图片发送成功"
            else:
                att = MIMEText("".join(attach_file['file_context']), 'base64')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = "'attachment; filename=" + attach_file['file_name'] + " '"
                msg.attach(att)
                status = "文件发送成功"
    server = smtplib.SMTP_SSL(os_env['HOST'], os_env['PORT'])
    server.login(os_env['USER'], os_env['PSWD'])
    server.sendmail(os_env["SENDER"], addresses, msg.as_string())
    server.quit
    return {
        "statusCode": 200,
        "body": json.dumps(status)
    }


def s3Read(bucket, key):
    client = boto3.client('s3')
    response = client.get_object(
        Bucket=bucket,
        Key=key,
    )
    content = response['Body'].read().decode()
    return content


def lambdaHandler(event, context):
    if event['type'] == "forget_password":
        email_status = sendEmail(addresses=event['address'],
                                 subject=event['subject'],
                                 content=s3Read(os_env['BUCKET'], os_env['KEY_PWD']),
                                 attach_files=event['attachment'],
                                 content_type="html")
        return email_status
    elif event['type'] == "test":
        email_status = sendEmail(addresses=event['address'],
                                 subject=event['subject'],
                                 content=s3Read(os_env['BUCKET'], os_env['KEY_FILE']),
                                 attach_files=event['attachment'],
                                 content_type="html")
        return email_status
