import os
import random
import redis
import json
import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders

# 1. first thing is to connect db, we use redis as tmp store
r = redis.StrictRedis(host='pharbers-cache.xtjxgq.0001.cnw1.cache.amazonaws.com.cn', port=6379, db=0)
# os.environ['USER'] = 'project@data-pharbers.com'
# os.environ['BUCKET'] = "ph-platform"
# os.environ['KEY_PWD'] = "2020-11-11/template/email/email-forgetpwd.html"
# os.environ['KEY_FILE'] = "2020-11-11/template/email/email.html"
# os.environ['PSWD'] = 'qiye@126'
# os.environ['HOST'] = 'smtp.ym.163.com'
# os.environ['PORT'] = '465'
# os.environ['SENDER'] = 'project@data-pharbers.com'
# os.environ['SENDER_NAME'] = "法伯科技"
# 2. other version
g_sender_name = os.environ["SENDER_NAME"]
g_host = os.environ["HOST"]
g_port = os.environ["PORT"]
g_username = os.environ["USER"]
g_pwd = os.environ["PSWD"]
g_sender = os.environ["SENDER"]
g_bucket = os.environ["BUCKET"]  # "ph-platform"
# g_key = "ph-platform"

# 3. global email ssl
server = smtplib.SMTP_SSL(g_host, g_port)
server.login(g_username, g_pwd)


def loadContent(ttype, address):
    type_key = {
        "forget_password": os.environ['KEY_PWD'],
        "test": os.environ['KEY_FILE']
    }
    func = {
        "forget_password": forgetPwdFunc,
        "test": tesFunc
    }

    client = boto3.client('s3')
    response = client.get_object(
        Bucket=g_bucket,
        Key=type_key[ttype]
    )
    return func[ttype](response['Body'].read().decode(), address)


def sendEmail(address, content_type, html_content, attachments=None, content_style='html'):  # 发送邮件
    msg = MIMEMultipart()
    msg.attach(MIMEText(html_content, content_style, 'utf-8'))
    msg['From'] = Header(g_sender_name)
    msg['To'] = Header(address, "utf-8")
    msg['Subject'] = Header(content_type, "utf-8")
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
    server.quit


def forgetPwdFunc(ctx, address):
    tmp = ''.join([str(random.randint(1, 9)) for i in range(6)])
    ctx = ctx.format("密码修改")
    ctx = ctx.replace("$$$URL$$$", "点击此处跳转修改密码页面")  # 更改URL名字
    ctx = ctx.replace("$$$URL_ADDRESS$$$", "https://www.accounts.pharbers.com:4200/resetPasswordPage/")
    # r.set(address, tmp)
    ctx = ctx.replace("$$$验证码$$$", tmp)
    return ctx


def tesFunc(ctx, address):
    tmp = ''.join([str(random.randint(1, 9)) for i in range(6)])
    r.set(address, tmp)
    return ctx.replace("$$$验证码$$$", tmp)


def lambdaHandler(event, context):  # 主函数入口
    result_code = 200
    result_message = {}
    # try:
    event = event['body']
    event = json.loads(event)
    for address in event['target_address']:
        sendEmail(address=address,
                  content_type=event['content_type'],
                  html_content=loadContent(event['content_type'], address),
                  attachments=event['attachments'],
                  content_style="html")
    result_message = {
        "status": "ok",
        "data": {
            "message": "seccessfully send emails"
        }
    }
    # except smtplib.SMTPServerDisconnected as e:
    #     result_message = {
    #         "status": "error",
    #         "error": {
    #             "message": "SMTP server disconnected"
    #         }
    #     }
    # except smtplib.SMTPResponseException as e:
    #     result_message = {
    #         "status": "error",
    #         "error": {
    #             "message": "SMTP server send email error"
    #         }
    #     }
    # except Exception as e:
    #     result_message = {
    #         "status": "error",
    #         "error": {
    #             "message": "Unknown Error"
    #         }
    #     }
    #
    # if result_message["status"] == "error":
    #     result_code = 503

    return {
        "statusCode": result_code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE",
        },
        "body": json.dumps(result_message)
    }
# if __name__ == "__main__":
#     data = {
#         "body": "{\"content_type\": \"forget_password\", \"target_address\": [\"2091038466@qq.com\"],\n  \"subject\": \"密码修改\",\n  \"attachments\": [{\"file_name\": \"test1.yaml\",\n    \"file_context\": [\"PH_NOTICE_EMAIL:\", \"metadata:\", \"name: PH_NOTICE_EMAIL\"]},\n    {\"file_name\": \"test2.txt\", \"file_context\": [\"xxxxxxxxxxxxxxxxxx\"]}]}"}
#     print(lambdaHandler(data, ' '))