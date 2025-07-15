import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from models import db, EmailRecord
from datetime import datetime

def send_tracked_email(sender, receiver, subject, body):
    msg = MIMEMultipart()
    msg['From'] = os.getenv("MAIL_USERNAME")
    msg['To'] = receiver.email
    msg['Subject'] = subject

    # Insert the tracking pixel
    tracking_url = f"{os.getenv('BASE_URL')}/tracker/{sender.id}/{receiver.id}"
    html_body = f"{body}<img src='{tracking_url}' width='1' height='1'/>"
    msg.attach(MIMEText(html_body, 'html'))

    # Save record
    record = EmailRecord(sender_id=sender.id, receiver_id=receiver.id, subject=subject, body=body)
    db.session.add(record)
    db.session.commit()

    # Send email
    server = smtplib.SMTP(os.getenv("MAIL_SERVER"), int(os.getenv("MAIL_PORT")))
    server.starttls()
    server.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
    server.send_message(msg)
    server.quit()
