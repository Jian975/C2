import email
import imaplib
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

def read_responses():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    status, messages = mail.search(None, '(UNSEEN SUBJECT "ResponseSubject")')
    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        print(msg.get_payload(decode=True).decode())
        mail.store(num, '+FLAGS', '\\Deleted')
        mail.expunge()

send_command('dir')
read_responses()