import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_command(command):
    msg = MIMEText(command)
    msg['Subject'] = 'TestSubject'
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    smtp = smtplib.SMTP_SSL('imap.gmail.com', 465)
    smtp.login(EMAIL, PASSWORD)
    smtp.sendmail(EMAIL, EMAIL, msg.as_string())
    smtp.quit()

send_command('dir')