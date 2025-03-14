import imaplib
from email import policy
from email.parser import BytesParser
import os
from pathlib import Path



def get_emails(email, password):
    username = email.split('@')[0]
    mail = imaplib.IMAP4('localhost')
    mail.login(username, password)
    mail.select('inbox')

    status, messages = mail.search(None, 'ALL')
    mail_ids = messages[0].split()
    emails = []

    for mail_id in mail_ids:
        status, msg_data = mail.fetch(mail_id, '(RFC822)')
        msg = BytesParser(policy=policy.default).parsebytes(msg_data[0][1])
        
        body = ""
        mail_file = None
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if "attachment" in content_disposition:
                    # Create a Path object
                    filename = part.get_filename()

                    if filename:
                        mail_file = f'./attachments/{mail_id}_{filename}' 
                        with open(mail_file, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                elif content_type == 'text/plain':
                    body += part.get_payload(decode=True).decode()
        else:
            body += part.get_payload(decode=True).decode()

        emails.append( {
            "from": msg["from"],
            "subject": msg["subject"],
            "body": body,
            "mail_id": mail_id,
            "attachment": mail_file
        })

    mail.logout()
    return emails
 