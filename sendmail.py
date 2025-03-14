import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os



def send_email(sender, receiver, subject, body, attachment):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Optional: Attach a file
    if attachment is not None:
        file_path = f'./{attachment.name}'
        with open(file_path, 'wb') as f:
            f.write(attachment.getbuffer())
        # Change this to the path of your file, if file doesn't exist, it will be ignored
        if os.path.exists(file_path):
            attachment = open(file_path, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
            msg.attach(part)
            attachment.close()
    
    with smtplib.SMTP('localhost', 25) as server:
        server.sendmail(sender, receiver, msg.as_string())

    os.remove(file_path)