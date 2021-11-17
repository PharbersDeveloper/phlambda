import os
import json
import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders

g_sender_name = os.getenv("SENDER_NAME")
g_host = os.getenv("HOST")
g_port = os.getenv("PORT")
g_username = os.getenv("USER")
g_pwd = os.getenv("PSWD")
g_sender = os.getenv("SENDER")
g_bucket = os.getenv("BUCKET")
g_key_pwd = os.getenv("KEY_PWD")
g_key_test = os.getenv("KEY_TEST")

server = smtplib.SMTP_SSL(g_host, g_port)
server.login(g_username, g_pwd)


def forgetPassword(html_content, code, url_tokens):  # 忘记密码html页面处理
    url = url_tokens
    html_content = html_content.replace("$$$验证码$$$", code)
    html_content = html_content.replace("$$$URL_ADDRESS$$$", url)
    html_content = html_content.replace("$$$URL$$$", "点击我修改密码")
    return html_content


def tes(html_content, code):
    pass


def loadContent(code, tokens, content_type):  # 选择获取哪个存储桶内容， 并处理网页内容
    func = {"forget_password": forgetPassword, "test": tes}
    key_choice = {"forget_password": g_key_pwd, "test": g_key_test}
    client = boto3.client('s3')
    response = client.get_object(Bucket=g_bucket, Key=key_choice[content_type])['Body'].read().decode()
    html_content = func[content_type](response, code, tokens)
    return html_content


def sendEmail(address, subject, html_content, attachments=[], content_style='html'):  # 发送邮件
    msg = MIMEMultipart()
    msg.attach(MIMEText(html_content, content_style, 'utf-8'))
    msg['From'] = Header(g_sender_name, 'utf-8')
    msg['To'] = Header(address, 'utf-8')
    msg['Subject'] = Header(subject, "utf-8")
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
    server.sendmail(g_sender, address, msg.as_string())


def lambdaHandler(event, context):  # 主函数入口
    result_code = 200
    result_message = {}
    try:
        event = event['body']
        if type(event) == str:
            event = json.loads(event)
        sendEmail(address=event["address"],
                  subject=event["subject"],
                  html_content=loadContent(event["code"], event["url_tokens"], event["content_type"]),
                  attachments=event["attachments"],
                  )
        result_message = {
            "status": "ok",
            "data": {
                "message": "seccessfully send emails"
            }
        }
    except smtplib.SMTPServerDisconnected as e:
        result_message = {
            "status": "error",
            "error": {
                "message": "SMTP server disconnected"
            }
        }
    except smtplib.SMTPResponseException as e:
        result_message = {
            "status": "error",
            "error": {
                "message": "SMTP server send email error"
            }
        }
    except Exception as e:
        result_message = {
            "status": "error",
            "data": {
                "message": "email send failure: " + str(e)
            }
        }
    if result_message["status"] == "error":
        result_code = 503
    return {
        "statusCode": result_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        },
        "body": json.dumps(result_message)
    }
