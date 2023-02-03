import smtplib
from datetime import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import *


def email_notify(sender, receivers, mail_subject, mail_content, sender_pass=None, html=True):
    # The mail addresses and password
    sender_address = sender
    sender_pass = sender_pass if sender_pass else getpass()
    receiver_addresses = receivers

    # Setup the MIME
    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = ",".join(receiver_addresses)
    message["Subject"] = mail_subject  # The subject line

    # The body and the attachments for the mail
    mode = "html" if html else "plain"
    message.attach(MIMEText(mail_content, mode))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_addresses, text)
    session.quit()
    print("Notification mail sent successfully.")
