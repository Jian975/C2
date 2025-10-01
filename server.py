import email
import imaplib
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from datetime import datetime

start_time = datetime.now()
imap_date = start_time.strftime("%d-%b-%Y")  # IMAP format: 24-Sep-2025
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
smtp = smtplib.SMTP_SSL('imap.gmail.com', 465)
smtp.login(EMAIL, PASSWORD)
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL, PASSWORD)

def send_command(command):
    msg = MIMEText(command)
    msg['Subject'] = 'Command'
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    smtp.sendmail(EMAIL, EMAIL, msg.as_string())

def read_responses():
    waiting = True
    while waiting:
        mail.select('inbox')
        _, messages = mail.search(None, f'(SINCE "{imap_date}" UNSEEN SUBJECT "Response")')
        if messages is not None:
            for num in messages[0].split():
                _, data = mail.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                print(msg.get_payload(decode=True).decode())
                mail.store(num, '+FLAGS', '\\Seen')
                mail.expunge()
                waiting = False

def is_blank (string):
    return not (string and string.strip())

def handle_input():
    cmd = input('> ')
    while cmd != 'quit':
        if not is_blank(cmd):
            send_command(cmd)
            read_responses()
        cmd = input('> ')

if '__main__' == __name__:
    handle_input()