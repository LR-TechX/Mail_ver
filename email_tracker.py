import smtplib
from email.mime.text import MIMEText
from models import db, EmailRecord
from datetime import datetime

def send_tracked_email(sender, receiver, subject, body):
    tracking_url = f"http://localhost:5000/tracker/{sender.id}/{receiver.id}"
    full_body = f'{body}<br><img src="{tracking_url}" width="1" height="1"/>'

    msg = MIMEText(full_body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender.email
    msg['To'] = receiver.email

    # Record in DB
    record = EmailRecord(sender_id=sender.id, receiver_id=receiver.id, subject=subject, body=body)
    db.session.add(record)
    db.session.commit()

    # SMTP Config (Change this for production)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('your-email@gmail.com', 'your-password')
        smtp.sendmail(sender.email, receiver.email, msg.as_string())
