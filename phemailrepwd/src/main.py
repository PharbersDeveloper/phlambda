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


def sendEmail(target_address, content_type,  html_content, attachments=None, content_style='plain'):
    status = {}
    for address in target_address:
        msg = MIMEMultipart()
        msg.attach(MIMEText(html_content, content_style, 'utf-8'))
        msg['From'] = Header(os_env["SENDER_NAME"])
        msg['To'] = Header(address, "utf-8")
        msg['Subject'] = Header(content_type, "utf-8")
        try:
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
                status = {"message": "file_success"}
            else:
                status = {"message": "password_change_success"}
        except:
            status = {"message": "file_send_failure"}
            return {
                "statusCode": 200,
                "body": json.dumps(status)
            }
        server = smtplib.SMTP_SSL(os_env['HOST'], os_env['PORT'])
        server.login(os_env['USER'], os_env['PSWD'])
        server.sendmail(os_env["SENDER"], address, msg.as_string())
        server.quit
    return {
        "statusCode": 200,
        "body": json.dumps(status)
    }


def s3Read(bucket, key):
    try:
        client = boto3.client('s3')
        response = client.get_object(
            Bucket=bucket,
            Key=key,
        )
        content = response['Body'].read().decode()
        return content
    except:
        return {
            "statusCode": 200,
            "body": json.dumps({"error": "S3_cant_request"})
        }


def typeChoice(event):
    if event['content_type'] == "forget_password":
        html_content = s3Read(os_env['BUCKET'], os_env['KEY_PWD'])
        if type(html_content) == str:
            html_content = html_content.format(event["subject"])
            email_status = sendEmail(target_address=event['target_address'],
                                     content_type=event['content_type'],
                                     html_content=html_content,
                                     content_style="html")
            return email_status
        else:
            return html_content
    elif event['content_type'] == "test":
        html_content = s3Read(os_env['BUCKET'], os_env['KEY_FILE'])
        if type(html_content) == str:
            html_content = html_content.format(event["subject"])
            email_status = sendEmail(target_address=event['target_address'],
                                     content_type=event['content_type'],
                                     html_content=html_content,
                                     attachments=event['attachments'],
                                     content_style="html")
            return email_status
        else:
            return html_content
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "no_this_content_type"})
        }


def lambdaHandler(event, context):
    try:
        event = event['body']
        event = json.loads(event)
        result = typeChoice(event)
    except Exception as e:
        return {"statusCode": 200, "body": json.dumps({"error": str(e)})}
    return result
