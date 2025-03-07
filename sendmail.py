import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

sender = 'user1@gmail.com'
receiver = 'user1@gmail.com'
subject = 'Test Email with Attachment'
body = 'This is a test email with an attachment sent from Python.'

# Create the email
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Optional: Attach a file
file_path = './image.webp'  # Change this to the path of your file, if file doesn't exist, it will be ignored
if os.path.exists(file_path):
    attachment = open(file_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
    msg.attach(part)
    attachment.close()

try:
    with smtplib.SMTP('localhost', 25) as server:
        server.sendmail(sender, receiver, msg.as_string())
    print('Email sent successfully.')
except Exception as e:
    print(f'Failed to send email: {e}')