import datetime
import pytz

from ktrains.korail.utils import convert_train_name as korail_convert_train_name
from ktrains.korail.utils import convert_station_name as korail_convert_station_name
from ktrains.korail.utils import station_names as korail_station_names
from ktrains.srt.utils import convert_station_name as srt_convert_station_name
from ktrains.srt.utils import station_names as srt_station_names


LINKS = {
    "korail": {
        "name": "Korail",
        "link": "https://www.letskorail.com",
        "login_link": "https://www.letskorail.com/korail/com/login.do",
        "reserve_link": "https://www.letskorail.com/ebizprd/EbizPrdTicketpr13500W_pr13510.do",
    },
    "srt": {
        "name": "SRT",
        "link": "https://etk.srail.kr",
        "login_link": "https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000",
        "reserve_link": "https://etk.srail.kr/hpg/hra/02/selectReservationList.do?pageId=TK0102010000",
    },
    "app": {
        "github": "https://github.com/fedebotu/k-trains",
        "streamlit": "http://k-trains.streamlit.app/",
        "email": "ktrains.app@gmail.com",
    },
}


def save_to_log(message, fname="log.txt"):
    with open(fname, "w") as f:
        f.write(message)


class Stations:
    def __init__(self, mode="korail", lang="en"):
        self.mode = mode
        self.lang = lang

    def station_names(self):
        if self.mode == "korail":
            return korail_station_names[self.lang]
        elif self.mode == "srt":
            return srt_station_names[self.lang]
        else:
            raise ValueError(
                f"Invalid mode: {self.mode}. Must be one of korail or srt."
            )

    def convert_station_name(self, station_name, lang=None):
        if lang is None:
            lang = self.lang
        if self.mode == "korail":
            return korail_convert_station_name(station_name, lang)
        elif self.mode == "srt":
            return srt_convert_station_name(station_name, lang)
        else:
            raise ValueError(
                f"Invalid mode: {self.mode}. Must be one of korail or srt."
            )

    def convert_train_name(self, train_name, lang=None):
        if lang is None:
            lang = self.lang
        if self.mode == "korail":
            return korail_convert_train_name(train_name, lang)
        elif self.mode == "srt":
            return train_name
        else:
            raise ValueError(
                f"Invalid mode: {self.mode}. Must be one of korail or srt."
            )


def current_time_timezone(to_timezone="Asia/Seoul", format=True):
    current_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    current_time = datetime.datetime.now(current_timezone)
    target_timezone = pytz.timezone(to_timezone)
    target_time = current_time.astimezone(target_timezone)
    if format:
        target_time = target_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    return target_time
