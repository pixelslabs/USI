import smtplib
from email.mime.text import MIMEText
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(subject, body, to_email):
    sender_email = EMAIL_USER
    sender_password = EMAIL_PASS  
  
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# Example Usage
send_email("Test Subject", "This is a test email",  TO_EMAIL)
