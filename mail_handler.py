import smtplib
import ssl
# from email.message import EmailMessage

"""
Parameter: content.
This function implements sending emails to the boss's mailbox.
We use smtp protocol.
"""
def send_email(content):
    port = 465
    smtp_server = "smtp.qq.com"
    sender_email = '295064001@qq.com'
    receiver_email = '295064001@qq.com'
    password = 'xgagvbvwfbpzcahj'
    message = "Your employee Jacob has starts working, content: " + content + '\n'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

