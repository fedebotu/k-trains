import argparse
import time as python_time

import chime
import streamlit as st

from ktrains.korail.korail import Korail
from ktrains.notify import email_notify
from ktrains.srt.srt import SRT
from ktrains.utils import save_to_log


def manage_available(train, email_sender, email_receivers, email_password, notify=True):
    subject = "Available!"
    print(subject)
    message = f"Train\n{train}\nhas seats now!"
    message += f"\nCurrent time: {python_time.strftime('%Y-%m-%d %H:%M:%S', python_time.localtime())}"
    if notify:
        email_notify(
            email_sender, email_receivers, subject, message, sender_pass=email_password
        )
    save_to_log(message)
    chime.info()


def manage_unavailable(
    train, email_sender, email_receivers, email_password, notify=True
):
    subject = "Sold out"
    print(subject)
    message = f"Train\n{train}\nhas no more seats now."
    message += f"\nCurrent time: {python_time.strftime('%Y-%m-%d %H:%M:%S', python_time.localtime())}"
    if notify:
        email_notify(
            email_sender, email_receivers, subject, message, sender_pass=email_password
        )
    save_to_log(message)
    chime.warning()


def manage_reservation(
    train, email_sender, email_receivers, email_password, notify=True
):
    subject = "Reserved!"
    print(subject)
    message = f"Train\n{train}\nhas been reserved! Complete the payment process on the app or website."
    message += f"\nCurrent time: {python_time.strftime('%Y-%m-%d %H:%M:%S', python_time.localtime())}"
    if notify:
        print("Sending reservation message")
        email_notify(
            email_sender, email_receivers, subject, message, sender_pass=email_password
        )
    save_to_log(message)
    chime.success()


def get_trains(
    id,
    pw,
    email_receivers,
    dep,
    arr,
    date,
    time,
    train_nos,
    mode="korail",
    notify=True,
    reserve=False,
    timeout=5,
    email_sender=None,
    email_password=None,
):
    try:
        print("Running main script!")

        if isinstance(notify, str):
            notify = notify.lower() == "true"
        if isinstance(reserve, str):
            reserve = reserve.lower() == "true"

        if email_sender is None:
            email_sender = st.secrets.get("email_sender")
        if email_password is None:
            email_password = st.secrets.get("email_password")

        if mode == "korail":
            ktrains = Korail(id, pw, auto_login=True)
        elif mode == "srt":
            ktrains = SRT(id, pw, auto_login=True)
        else:
            raise ValueError(f"Invalid mode: {mode}. Must be one of korail or srt.")

        # comma separated list of train numbers
        train_nos = train_nos.split(",")
        email_receivers = email_receivers.split(",")

        train_availability = {train_no: False for train_no in train_nos}

        while True:
            trains = ktrains.search_train(dep, arr, date, time, available_only=False)

            # Filter out trains that are not in train_codes
            trains = [train for train in trains if train.train_number in train_nos]
            for train in trains:
                was_available = train_availability[train.train_number]

                if not was_available and train.seat_available():
                    if reserve:
                        ktrains.reserve(train)
                        manage_reservation(
                            train, email_sender, email_receivers, email_password, notify
                        )
                        print("Reserved. Exiting...")
                        return
                    else:
                        manage_available(
                            train, email_sender, email_receivers, email_password, notify
                        )
                    train_availability[train.train_number] = True

                elif was_available and not train.seat_available():
                    manage_unavailable(
                        train, email_sender, email_receivers, email_password, notify
                    )
                    train_availability[train.train_number] = False
                else:
                    pass  # do nothing

            # sleep for timeout seconds
            python_time.sleep(timeout)

    except Exception as e:
        print("Error:\n" + str(e))
        save_to_log("Error:\n" + str(e))
        chime.error()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=str, required=True)
    parser.add_argument("--pw", type=str, required=True)
    parser.add_argument("--email-receivers", type=str, required=True)
    parser.add_argument("--dep", type=str, required=True)
    parser.add_argument("--arr", type=str, required=True)
    parser.add_argument("--date", type=str, required=True)
    parser.add_argument("--time", type=str, required=True)
    parser.add_argument("--train-nos", type=str, required=True)
    parser.add_argument("--mode", type=str, default="korail")
    parser.add_argument("--notify", type=str, default="True")
    parser.add_argument("--reserve", type=str, default="False")
    parser.add_argument("--timeout", type=int, default=5)
    parser.add_argument("--email-sender", type=str, default=None)
    parser.add_argument("--email-password", type=str, default=None)
    args = parser.parse_args()

    print(args)
    print(vars(args))
    get_trains(**vars(args))
