import imaplib
from email import policy
from email.parser import BytesParser

username = 'user1'
password = '12345'

try:
    mail = imaplib.IMAP4('localhost')
    mail.login(username, password)
    mail.select('inbox')

    status, messages = mail.search(None, 'ALL')
    mail_ids = messages[0].split()

    for mail_id in mail_ids:
        mail.store(mail_id, '+FLAGS', '\\Deleted')
    mail.expunge()
    print("Emails and attachments deleted permanently.")
    mail.logout()
except Exception as e:
    print(f'Failed to retrieve emails: {e}')