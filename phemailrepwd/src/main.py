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


def sendEmail(target_address, content_type, content, attachments=None, content_style='html',
              sender_name=os_env['SENDER_NAME']):
    for address in target_address:
        status = {"message": "password_change_sucess"}
        msg = MIMEMultipart()
        msg['From'] = Header(sender_name, 'utf-8')
        msg['To'] = Header(address)
        msg['Subject'] = Header(content_type)
        msg.attach(MIMEText(content, content_style, 'utf-8'))
        if attachments is not None:
            for attach_file in attachments:
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
            status = {"message": "file_sucess"}
        server = smtplib.SMTP_SSL(os_env['HOST'], os_env['PORT'])
        server.login(os_env['USER'], os_env['PSWD'])
        server.sendmail(os_env["SENDER"], address, msg.as_string())
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
    event = event['body']
    event = json.loads(event)
    if event['content_type'] == "forget_password":
        email_status = sendEmail(target_address=event['target_address'],
                                 content_type=event['content_type'],
                                 content=s3Read(os_env['BUCKET'], os_env['KEY_PWD']),
                                 content_style="html")
        return email_status
    elif event['content_type'] == "test":
        email_status = sendEmail(target_address=event['target_address'],
                                 content_type=event['content_type'],
                                 content=s3Read(os_env['BUCKET'], os_env['KEY_FILE']),
                                 attachments=event['attachments'],
                                 content_style="html")
        return email_status
