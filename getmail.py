import imaplib
import email
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
        status, msg_data = mail.fetch(mail_id, '(RFC822)')
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])
        
        print(f'From: {msg["from"]}')
        print(f'Subject: {msg["subject"]}')
        print('Body:')
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        with open(filename, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        print(f'Saved attachment to current working directory: {filename}')
                elif content_type == 'text/plain':
                    print(part.get_payload(decode=True).decode())
        else:
            print(msg.get_payload(decode=True).decode())
        
        print('-' * 50)

    mail.logout()
except Exception as e:
    print(f'Failed to retrieve emails: {e}')