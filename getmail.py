import imaplib
from email import policy
from email.parser import BytesParser



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
        
        text_result = f'From: {msg["from"]}\nSubject: {msg["subject"]}\nBody: '
        mail_file = None
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        mail_file = "./attachments/" + filename + f"_{mail_id}"
                        with open(mail_file, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                elif content_type == 'text/plain':
                    text_result += part.get_payload(decode=True).decode()
        else:
            text_result += part.get_payload(decode=True).decode()

        emails.append( {
            "mail_id": mail_id,
            "text_result": text_result,
            "attachment": mail_file
        })

    mail.logout()
    return emails
 