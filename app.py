import datetime
import subprocess
import sys
from copy import deepcopy
import gettext

_ = gettext.gettext
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import streamlit.components.v1 as components

from ktrains.korail.korail import Korail
from ktrains.srt.srt import SRT
from ktrains.utils import Stations, save_to_log, LINKS

language = st.sidebar.selectbox(
    _("Select your language"), ["English", "한국어", "Italiano", "Español"]
)
if language == "English":
    language = "en"
elif language == "한국어":
    language = "kr"
elif language == "Español":
    language = "es"
elif language == "Italiano":
    language = "it"

try:
    localizator = gettext.translation("base", localedir="locales", languages=[language])
    localizator.install()
    _ = localizator.gettext
except:
    pass

# Dictionary of functions
name_to_class = {
    "korail": Korail,
    "srt": SRT,
}


if "ktrains" not in st.session_state:
    st.session_state.ktrains = None
if "mode" not in st.session_state:
    st.session_state.mode = "korail"
if "id" not in st.session_state:
    st.session_state.id = ""
if "pw" not in st.session_state:
    st.session_state.pw = ""
if "trains" not in st.session_state:
    st.session_state.trains = None
if "email_receivers" not in st.session_state:
    st.session_state.email_receivers = ""
if "pid" not in st.session_state:
    st.session_state.pid = None
if "search_date" not in st.session_state:
    st.session_state.search_date = None
if "running" not in st.session_state:
    st.session_state.running = False
if "previous_log" not in st.session_state:
    st.session_state.previous_log = ""
if "cur_date" not in st.session_state:
    st.session_state.cur_date = datetime.date.today()
if "cur_time" not in st.session_state:
    st.session_state.cur_time = datetime.datetime.now()


def check_login():
    if st.session_state.ktrains is None:
        return False
    else:
        if st.session_state.ktrains.is_login:
            return True
    return False


st.title("K-trains 🇰🇷-🚄")
st.markdown(_("Fork me on:") + f" [{_('GitHub')}]({LINKS['app']['github']})")

if not check_login():
    # Login page
    # Checkbox with two options and an image on top of each
    mode = st.selectbox(_("Select railways company"), [_("Korail"), _("SRT")]).lower()
    st.session_state.mode = mode.lower()
    st.write(
        _("Get your credentials from {} website: [{}]({})").format(
            LINKS[mode]["name"], LINKS[mode]["link"], LINKS[mode]["link"]
        )
    )
    col1, col2 = st.columns(2)
    st.session_state.id = col1.text_input(_("ID"), st.session_state.id, key="username")
    st.session_state.pw = col2.text_input(_("PW"), st.session_state.pw, type="password", key="password")
    login_button = st.button(_("Login"))
    if login_button:
        KTrains = name_to_class[st.session_state.mode]
        ktrains = KTrains(st.session_state.id, st.session_state.pw, auto_login=True)
        st.session_state.ktrains = ktrains
        if check_login():
            # refresh page
            st.rerun()
        else:
            st.error(_("Login failed"))
else:
    if language == "kr":
        language_sched = "kor"
    else:
        language_sched = "en"

    # What happens when logged in
    mode = st.session_state.mode
    stations = Stations(mode, language_sched)

    # Login and logout
    st.success(_("Logged in successfully to {}").format(mode.upper()))
    col1, col2 = st.columns(2)
    with col1:
        st.write(_("Logged in as: {}").format(st.session_state.id))
    with col2:
        logout_button = st.button(_("Logout"))
        if logout_button:
            st.session_state.ktrains.logout()
            st.session_state.ktrains = None
            st.rerun()
    # divider
    st.markdown("""---""")

    # Main layout
    ktrains = st.session_state.ktrains

    stations_names = stations.station_names()
    stations_names = list(map(str, stations_names))
    if 'dep_index' not in st.session_state or 'arr_index' not in st.session_state:
        if mode == "korail":
            st.session_state.dep_index = 107
            st.session_state.arr_index = 44
        else:
            st.session_state.dep_index = 0
            st.session_state.arr_index = 5

    col1, swap_col, col2 = st.columns([1, 0.2, 1])
    swap_col.write(" ")
    if swap_col.button("⇄"):
        # Swap the values in session state
        st.session_state.dep_index, st.session_state.arr_index = st.session_state.arr_index, st.session_state.dep_index
        dep = stations_names[st.session_state.dep_index]
        arr = stations_names[st.session_state.arr_index]
        # Use session state for indices
    dep = col1.selectbox(_("Departure"), stations_names, index=st.session_state.dep_index)
    arr = col2.selectbox(_("Arrival"), stations_names, index=st.session_state.arr_index)

    col1, col2 = st.columns(2)
    date = col1.date_input("Date", value=st.session_state.cur_date)
    time = col2.time_input("Time", value=st.session_state.cur_time)
    st.session_state.cur_date = date
    st.session_state.cur_time = time
    date = date.strftime("%Y%m%d")
    time_selected = time.strftime("%H%M%S")
    #time = time.strftime("%H%M%S")
    time = "000000"

    table_stations = Stations(mode, language_sched)
    if st.button(_("Search")):
        trains = ktrains.search_train(stations.convert_station_name(dep), stations.convert_station_name(arr), date, time, available_only=False)
        if trains == []:
            st.error("No trains found")
            st.session_state.trains = None
        else:
            # stations.convert_station_name(trains[0].dep_station_name, lang="en")
            train_list = []
            for train in trains:
                if language != "kr":
                    table_lang = "tc"
                else:
                    table_lang = "kr"
                train_list.append(
                    {
                        "train_no": train.train_number,
                        "train_type_name": stations.convert_train_name(
                            train.train_name, lang=table_lang
                        ),
                        "dep_name": stations.convert_station_name(
                            train.dep_station_name, lang=table_lang
                        ),
                        "arr_name": stations.convert_station_name(
                            train.arr_station_name, lang=table_lang
                        ),
                        "dep_time": train.dep_time,
                        "arr_time": train.arr_time,
                        "duration": None,
                        "has_general_seat": train.general_seat_available(),
                        "has_special_seat": train.special_seat_available(),
                        "reserve_possible_name": None
                        if not hasattr(train, "reserve_possible_name")
                        else train.reserve_possible_name,
                    }
                )
            st.session_state.trains = pd.DataFrame(train_list)
            st.session_state.search_date = date

# Main train selection
if st.session_state.trains is not None:
    df = deepcopy(st.session_state.trains)

    df["duration"] = pd.to_datetime(df["arr_time"], format="%H%M%S") - pd.to_datetime(
        df["dep_time"], format="%H%M%S"
    )
    df["duration"] = df["duration"].apply(lambda x: str(x)[7:-3])
    df["dep_time"] = pd.to_datetime(df["dep_time"], format="%H%M%S").dt.strftime(
        "%H:%M"
    )
    df["arr_time"] = pd.to_datetime(df["arr_time"], format="%H%M%S").dt.strftime(
        "%H:%M"
    )

    # Convert dep_name, arr_name, dep_time, arr_time, duration to a string like (dep_name) (dep_time) -> (arr_name) (arr_time) (duration)
    df["schedule"] = df["dep_name"] + "→" + df["arr_name"]
    df["time"] = df["dep_time"] + "→" + df["arr_time"]

    df["has_general_seat"] = df["has_general_seat"].apply(lambda x: "✓" if x else "✗")
    df["has_special_seat"] = df["has_special_seat"].apply(lambda x: "✓" if x else "✗")
    df["normal/special_seat"] = df["has_general_seat"] + " / " + df["has_special_seat"]

    df = df.drop(
        columns=[
            "has_general_seat",
            "has_special_seat",
            "dep_name",
            "arr_name",
            "dep_time",
            "arr_time",
        ]
    )
    df = df.iloc[:, [0, 1, 4, 5, 2, 6, 3]]

    df.columns = [
        _("No"),
        _("Type"),
        _("Schedule"),
        _("Time"),
        _("Duration"),
        _("Normal/Special Seat"),
        _("Price"),
    ]

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gd.build()

    # If date is not none, set it as title
    # 20230202 -> 2023-02-02
    date = st.session_state.search_date
    if date is not None:
        date_formatted = date[:4] + "/" + date[4:6] + "/" + date[6:]
        st.write(_("Search results for {}:").format(date_formatted))

    # Split the dataframe into chunks for pagination
    if 'current_chunk_index' not in st.session_state:
        st.session_state['current_chunk_index'] = 0

    if 'current_selected_time' not in st.session_state:
        st.session_state['current_selected_time'] = "111111"

    # Check if DataFrame is not empty
    flag_time = time_selected
    if not df.empty:
        chunk_size = 10  # Default chunk size
        if len(df) < chunk_size:
            chunk_size = len(df)
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        total_chunks = len(chunks)

        #Time changed
        if st.session_state['current_selected_time'] != time_selected:
            st.session_state['current_selected_time'] = time_selected
            for i, chunk in enumerate(chunks):
                times_chunks = chunk['Time'].str[:2]
                if time_selected[:2] in times_chunks.tolist():
                    st.session_state['current_chunk_index'] = i
                    break
        
        # Assuming grid_options is defined and AgGrid is imported
        grid_return = AgGrid(
            chunks[st.session_state['current_chunk_index']],
            gridOptions=grid_options,
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True,
            columns_auto_size_mode=2,
            enable_enterprise_modules=False,
            header_checkbox_selection_filtered_only=True,
            theme="streamlit",
            use_checkbox=True,
            width="200%",
        )
        
        # Navigation Buttons
        kol2, kol1, kol3 = st.columns([0.7, 1, 1])
        
        # Previous Button
        with kol1:
            if st.session_state['current_chunk_index'] > 0 and st.button("<- Previous"):
                st.session_state['current_chunk_index'] -= 1
                st.experimental_rerun()
        
        # Next Button
        with kol3:
            if st.session_state['current_chunk_index'] < total_chunks - 1 and st.button("Next ->"):
                st.session_state['current_chunk_index'] += 1
                st.experimental_rerun()


    new_df = pd.DataFrame(grid_return["selected_rows"])

    # get train_codes from new df
    if not new_df.empty:
        train_codes = new_df.iloc[:, 1].tolist()
        # st.write(train_codes)

    st.header(_("Runner Settings"))
    st.write(
        _(
            "The app will automatically reserve and/or notify you when the train is available."
        )
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(_("Reserve settings"))
        st.markdown(
            _(
                "Reserve the train(s) automatically. You will need to reserve in the app/website within a few minutes."
            )
            + f" ([link]({LINKS[mode]['reserve_link']}))"
        )

        st.write(
            _(
                "If you do not process the payment, the reservation will be cancelled automatically."
            )
        )
        st.number_input(
            _("Number of tickets"),
            min_value=1,
            max_value=10,
            value=1,
            step=1,
            key="num_tickets",
        )

        st.write(
            _(
                "Please select the preferred seat type. If both are selected, the app will try to reserve the first available."
            )
        )
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            general_seat = st.checkbox(
                _("General seat"), key="general_seat", value=True
            )
        with sub_col2:
            special_seat = st.checkbox(
                _("Special seat"), key="special_seat", value=True
            )
        if general_seat and not special_seat:
            seat_type = "R"
        elif not general_seat and special_seat:
            seat_type = "S"
        else:
            seat_type = "B"
    with col2:
        st.subheader(_("Email notifications settings"))
        st.write(_("Notify you when the train is available."))
        st.write(
            _(
                "Receivers are the email addresses that will receive notifications. Use commas to separate multiple addresses."
            )
        )
        st.write(
            _("Note: sender email is ")
            + f" {LINKS['app']['email']} ."
            + _(" Be sure to check your spam folder.")
        )
        email_receivers = st.text_input(
            _("Receivers"), st.session_state.email_receivers
        )
        st.session_state.email_receivers = email_receivers

    col1, col2 = st.columns(2)
    with col1:
        st.write(_("Check to reserve the ticket."))
        st.checkbox(_("Reserve"), key="reserve", value=True)
    with col2:
        st.write(_("Check to Notify to email."))
        st.checkbox(_("Notify"), key="notify", value=True)

    st.markdown("---")

    if st.button(_("Submit")):
        if email_receivers == "" and st.session_state.notify:
            st.error(_("Please set receiver(s) email in the sidebar"))
        elif new_df.empty:
            st.error(_("Please select at least one train"))
        else:
            # Run as a subprocess
            # make train codes to string with comma
            train_codes_ = ",".join(train_codes)
            command = [
                sys.executable,
                "reserve.py",
                "--id",
                st.session_state.id,
                "--pw",
                st.session_state.pw,
                "--email-receivers",
                email_receivers,
                "--dep",
                stations.convert_station_name(dep),
                "--arr",
                stations.convert_station_name(arr),
                "--date",
                date,
                "--time",
                time,
                "--train-nos",
                train_codes_,
                "--mode",
                st.session_state.mode,
                "--notify",
                str(st.session_state.notify),
                "--reserve",
                str(st.session_state.reserve),
                "--number-of-tickets",
                str(st.session_state.num_tickets),
                "--seat-type",
                seat_type,
            ]
            print(" ".join(command))
            pid = subprocess.Popen(command)  # open in background
            st.session_state.running = True
            st.session_state.pid = pid
            save_to_log("")  # clear log
            st.write(_("Running..."))

# If running, show log
if st.session_state.running:
    st.write(
        _("Hang tight, I'm running... This may take some time, until we find a train!")
    )
    st.markdown("---")
    st.write(_("Log:"))
    with open("log.txt", "r") as f:
        log = f.read()
        if st.session_state.previous_log != log:
            st.session_state.previous_log = log
            st.write(log)

    # Stop runner
    st.markdown("---")
    if st.button(_("Stop runner")):
        if st.session_state.pid is not None:
            st.session_state.pid.terminate()
            st.success(_("Stopped"))
            st.session_state.running = False
        else:
            st.error(_("No process running"))
