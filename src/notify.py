from datetime import *
from getpass import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def notify(sender, receivers, mail_content, sender_pass=None):

    today = date.today()
        
    # The mail addresses and password
    sender_address = sender
    sender_pass = sender_pass if sender_pass else getpass() 
    receiver_addresses = receivers
    
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ",".join(receiver_addresses)
    message['Subject'] = f"[Notice] Change in status of the train ({str(today.strftime('%b %Y'))})" # trends investigation and data statistics time reduction 
                                   
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)       # use gmail with port
    session.starttls()                                  # enable security
    session.login(sender_address, sender_pass)          # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_addresses, text)
    session.quit()
    print('Notification mail is successfully sent.')

# if __name__ == '__main__':
#     sender = 'berto.federico2@gmail.com'  # insert sender address here
#     receivers = [
#                  'fberto@kaist.ac.kr',
#                  'berto.federico2@hotmail.com'
#                  ]  # insert receiver addresses here
#     file_name = "data/conferences.csv"                      # conference schedule file (to be checked)
#     # sends email if upcoming conference exists
#     if filter(file_name):
#         notify(sender, receivers, file_name[:-4] + '_' + str(date.today()) + '.csv')
#         os.remove(file_name[:-4] + '_' + str(date.today()) + '.csv')
#     else:
#         print('No upcoming conference, no email sent.')