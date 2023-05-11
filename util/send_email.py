import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_email_username = os.environ['from_email_username']
from_email_password = os.environ['from_email_password']
smtp_server = os.environ['smtp_server']


def email_forgot_password_otp(otp, to_email):
    # try:
    message = MIMEMultipart()
    message["Subject"] = "Reset Password"
    message["From"] = from_email_username
    message["To"] = to_email
    print(from_email_username)
    print(from_email_password)
    msg_text = f"""Please use this OTP to change your password: {otp}"""
    msg_mime_text = MIMEText(msg_text, "plain")
    message.attach(msg_mime_text)
    connection = smtplib.SMTP(smtp_server, 587)
    connection.starttls()
    connection.login(user=from_email_username, password=from_email_password)
    connection.sendmail(from_addr=from_email_username, to_addrs=to_email, msg=message.as_string())
    connection.close()
    return True
    # except Exception as e:
    #     print(e)
    #     return False
