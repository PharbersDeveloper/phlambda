import os
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
server = smtplib.SMTP_SSL(g_host, g_port)
server.login(g_username, g_pwd)


def send_email(address, subject, content, receiver, attach_files=None, content_type='plain'):
    # version2

    msg = MIMEMultipart()
    msg['From'] = Header(g_sender_name, 'utf-8')
    msg['To'] = Header(receiver)
    msg['Subject'] = Header(subject)
    msg.attach(MIMEText(content, content_type, 'utf-8'))

    # if attach_files is not None:
    #     for attach_file in attach_files:
    #         if attach_file['file_name'].endswith('png'):
    #             # 设置附件的MIME和文件名，这里是png类型:
    #             att = MIMEBase('image', 'png', filename=attach_file['file_name'])
    #             # 加上必要的头信息:
    #             att.add_header('Content-Disposition', 'attachment', filename=attach_file['file_name'])
    #             att.add_header('Content-ID', '<0>')
    #             att.add_header('X-Attachment-Id', '0')
    #             # 把附件的内容读进来:
    #             att.set_payload(attach_file['file_context'])
    #             # 用Base64编码:
    #             encoders.encode_base64(att)
    #             msg.attach(att)
    #         else:
    #             att = MIMEText("".join(attach_file['file_context']), 'base64')
    #             att["Content-Type"] = 'application/octet-stream'
    #             att["Content-Disposition"] = "'attachment; filename=" + attach_file['file_name'] + " '"
    #             msg.attach(att)

    server.sendmail(g_sender, address, msg.as_string())
    server.quit()


def lambda_handler(event, context):  # 主函数入口

    components = event["components"]
    l1 = []
    for component in components:
        l1.append(component["prefix"].split("/")[-1])

    if event["status"] == "success":
        content = "本次CICD部署成功，部署Id为" + event["executionName"] +", 发布的项目有: " + ",".join(l1)
    else:
        content = "本次CICD部署失败，部署Id为" + event["executionName"] +", 发布的项目有: " + ",".join(l1)
    send_email(
        address=event["email"],
        subject="前端CICD结果",
        content=content,
        receiver=event["publisher"]
    )
    return True
