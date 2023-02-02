from ktrains.korail.utils import convert_station_name as korail_convert_station_name
from ktrains.korail.utils import station_names as korail_station_names
from ktrains.srt.utils import convert_station_name as srt_convert_station_name
from ktrains.srt.utils import station_names as srt_station_names


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
