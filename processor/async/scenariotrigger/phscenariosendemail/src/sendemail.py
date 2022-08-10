import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from genHtml import getResultHTML
import os

my_sender = os.getenv("SENDMAILBOX")    # 发件人邮箱账号
my_pass = os.getenv("SENDPW")              # 发件人邮箱密码
my_user = os.getenv("TOMAILBOX")       # 收件人邮箱账号，我这边发送给自己
sendNickName = os.getenv("SENDNICKNAME")
ToNickName = os.getenv("TONICKNAME")

def SendEmail(Result):
    try:
        mail_msg = getResultHTML(Result)
        msg = MIMEText(mail_msg, 'html','utf-8')
        msg['From'] = formataddr([sendNickName, my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([ToNickName, my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "Pharbers ScenarioTrigger Notice"                # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.ym.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception as e:
        print("*"*50 + "ERROR" + "*"*50, str(e))
        print("邮件发送失败")
