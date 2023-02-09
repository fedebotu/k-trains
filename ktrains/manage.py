import chime

from ktrains.notify import create_email, email_notify
from ktrains.utils import save_to_log, current_time_timezone


def manage_available(train, email_sender, email_receivers, email_password, notify=True):
    subject = "Available!"
    print(subject)
    message = f"Train<br>{train}<br>has seats now!"
    message += f"<br><small>Current time: {current_time_timezone()}</small>"
    if notify:
        html = create_email(subject, message, reserve=False)
        email_notify(
            email_sender, email_receivers, subject, html, sender_pass=email_password
        )
    save_to_log(message)
    chime.info()


def manage_unavailable(
    train, email_sender, email_receivers, email_password, notify=True
):
    subject = "Sold out"
    print(subject)
    message = f"Train\n{train}\nhas no more seats now."
    message += f"<br><small>Current time: {current_time_timezone()}</small>"
    if notify:
        html = create_email(subject, message, reserve=False)
        email_notify(
            email_sender, email_receivers, subject, html, sender_pass=email_password
        )
    save_to_log(message)
    chime.warning()


def manage_reservation(
    train, email_sender, email_receivers, email_password, notify=True, mode="korail"
):
    subject = "Reserved!"
    print(subject)
    message = f"Train<br>{train}<br>has been reserved! Complete the payment process on the app or website as soon as possible (in 10 or 20 minutes)."
    message += f"<br><small>Time of reservation (KST): {current_time_timezone()}</small>"

    if notify:
        print("Sending reservation message")
        html = create_email(subject, message, reserve=True, mode=mode)
        email_notify(
            email_sender, email_receivers, subject, html, sender_pass=email_password
        )
    save_to_log(message)
    chime.success()


def manage_start(
    trains, email_sender, email_receivers, email_password, notify=True, mode="korail"
):  
    # check if list
    if not isinstance(trains, list):
        trains = [trains]

    subject = "K-Trains application started!"
    message = f"This email is to notify you that the K-Trains application has started. Checking for the following trains:<br>"
    for train in trains:
        message += f"{train}<br>"
    message += f"<br> You will receive another email when a train is available or when a train is reserved.<br>If you are running the app on a server, you can close the window now."
    message += f"<br><small>Current time: {current_time_timezone()}</small>"

    if notify:
        print("Sending start message")
        html = create_email(subject, message, reserve=False, mode=mode)
        email_notify(
            email_sender, email_receivers, subject, html, sender_pass=email_password
        )
    save_to_log(message)
    chime.info()


def manage_error(
    train, email_sender, email_receivers, email_password, notify=True, mode="korail"
):
    subject = "Error occurred"
    print(subject)
    message = f"An error occurred while running the app:<br><a style='color: #FFBABA;'>{train}</a><br>. Please check whether all your trains were reserved or try re-running the app."
    message += f"<br><small>Current time: {current_time_timezone()}</small>"

    if notify:
        print("Sending error message")
        html = create_email(subject, message, reserve=False, mode=mode)
        email_notify(
            email_sender, email_receivers, subject, html, sender_pass=email_password
        )
    save_to_log(message)
    chime.error()