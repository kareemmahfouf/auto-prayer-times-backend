from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# get sender email's username and password
load_dotenv()
email_username = os.getenv("EMAIL_USERNAME")
email_password = os.getenv("EMAIL_PASSWORD")


def send_email(message, recipient):
    # construct email
    email = MIMEMultipart()
    email["From"] = email_username
    email["To"] = recipient
    email["Subject"] = "Today's Prayer Times"
    email.attach(MIMEText(message, "html"))

    # connect to gmail SMTP
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, recipient, str(email))
    except smtplib.SMTPException:
         raise
