import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025

SENDER_ADDRESS = "placementportal@ppa.com"
SENDER_PASSWORD = ""


def send_email(to_address, subject, message):

    msg = MIMEMultipart()

    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(
        MIMEText(message, "html")
    )

    smtp = smtplib.SMTP(

        host=SMTP_SERVER_HOST,

        port=SMTP_SERVER_PORT

    )

    smtp.send_message(msg)

    smtp.quit()