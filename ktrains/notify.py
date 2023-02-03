import smtplib
from datetime import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import *

from ktrains.utils import LINKS


TEMPLATE_FILE = "assets/email-template.html"


def create_email(subject, message, reserve=False, mode="korail"):
    with open(TEMPLATE_FILE, "r") as f:
        html = f.read()
    button_message = (
        "Complete reservation here!"
        if reserve
        else f"Go to {LINKS[mode]['name']} website"
    )
    link = LINKS[mode]["reserve_link"] if reserve else LINKS[mode]["link"]
    html = html.replace("{{subject}}", subject)
    html = html.replace("{{message}}", message)
    html = html.replace(
        "{{link}}", f'<td> <a href="{link}" target="_blank">{button_message}</a> </td>'
    )
    return html


def email_notify(
    sender, receivers, mail_subject, mail_content, sender_pass=None, html=True
):
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
