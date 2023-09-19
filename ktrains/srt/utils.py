station_names_korean = [
    "수서",
    "동탄",
    "지제",
    "천안아산",
    "오송",
    "대전",
    "공주",
    "익산",
    "정읍",
    "광주송정",
    "나주",
    "목포",
    "김천구미",
    "서대구",
    "동대구",
    "신경주",
    "울산(통도사)",
    "울산",
    "통도사",
    "부산",
]
station_names_english = [
    "Suseo",
    "Dongtan",
    "Jije",
    "Cheonan-Asan",
    "Osong",
    "Daejeon",
    "Gongju",
    "Iksan",
    "Jeongeup",
    "Gwangju-Songjeong",
    "Naju",
    "Mokpo",
    "Gimcheon-Gumi",
    "Seodaegu",
    "Dongdaegu",
    "Singyeongju",
    "Ulsan (Tongdosa)",
    "Ulsan",
    "Tongdosa",
    "Busan",
]

station_names = {"kor": station_names_korean, "en": station_names_english}


def convert_station_name(station_name, lang="en"):
    if lang == "en":
        # get index of station_name in station_names_english
        index = station_names_english.index(station_name)
        return station_names_korean[index]
    elif lang == "tc":
        index = station_names_korean.index(station_name)
        return station_names_english[index]
    else:
        return station_name
