import datetime
import subprocess
import sys
from copy import deepcopy

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from ktrains.korail.korail import Korail
from ktrains.srt.srt import SRT
from ktrains.utils import Stations, save_to_log, LINKS

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


def check_login():
    if st.session_state.ktrains is None:
        return False
    else:
        if st.session_state.ktrains.is_login:
            return True
    return False


st.title("K-trains 🇰🇷-🚄")


# st.sidebar.title("Settings")

# Sidebar
# language = st.sidebar.selectbox("Select language", ["en", "kor"])

# st.sidebar.subheader("Email settings")
# st.sidebar.write(
#     "Receivers are the email addresses that will receive notifications. Use commas to separate multiple addresses."
# )
# email_receivers = st.sidebar.text_input("Receivers", st.session_state.email_receivers)
# st.session_state.email_receivers = email_receivers

if not check_login():
    # Login page
    # Checkbox with two options and an image on top of each
    mode = st.selectbox("Select railways company", ["Korail", "SRT"]).lower()
    st.session_state.mode = mode.lower()
    st.write(
        "Get your credentials from {} website: [{}]({})".format(
            LINKS[mode]["name"], LINKS[mode]["link"], LINKS[mode]["link"]
        )
    )
    col1, col2 = st.columns(2)
    st.session_state.id = col1.text_input("ID", st.session_state.id)
    st.session_state.pw = col2.text_input("PW", st.session_state.pw, type="password")
    login_button = st.button("Login")
    if login_button:
        KTrains = name_to_class[st.session_state.mode]
        ktrains = KTrains(st.session_state.id, st.session_state.pw, auto_login=True)
        st.session_state.ktrains = ktrains
        if check_login():
            # refresh page
            st.experimental_rerun()
        else:
            st.error("Login failed")
else:
    language = st.selectbox("Select language", ["en", "kor"])

    # What happens when logged in
    mode = st.session_state.mode

    stations = Stations(mode, language)

    # Login and logout
    st.success("Logged in successfully to {}".format(mode.upper()))
    col1, col2 = st.columns(2)
    with col1:
        st.write("Logged in as: {}".format(st.session_state.id))
    with col2:
        logout_button = st.button("Logout")
        if logout_button:
            st.session_state.ktrains.logout()
            st.session_state.ktrains = None
            st.experimental_rerun()
    # divider
    st.markdown("""---""")

    # Main layout
    ktrains = st.session_state.ktrains

    # Set with two columns
    col1, col2 = st.columns(2)
    dep = col1.selectbox(
        "Departure", stations.station_names(), index=107 if mode == "korail" else 0
    )
    arr = col2.selectbox(
        "Arrival", stations.station_names(), index=44 if mode == "korail" else 5
    )
    dep = stations.convert_station_name(dep)
    arr = stations.convert_station_name(arr)

    col1, col2 = st.columns(2)
    date = col1.date_input("Date", value=datetime.date.today())
    time = col2.time_input("Time", value=datetime.datetime.now())
    date = date.strftime("%Y%m%d")
    time = time.strftime("%H%M%S")

    if st.button("Search"):
        trains = ktrains.search_train(dep, arr, date, time, available_only=False)
        if trains == []:
            st.error("No trains found")
            st.session_state.trains = None
        else:
            train_list = []
            for train in trains:
                train_list.append(
                    {
                        "train_no": train.train_number,
                        "train_type_name": train.train_name,
                        "dep_name": train.dep_station_name,
                        "arr_name": train.arr_station_name,
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
        "No",
        "Type",
        "Schedule",
        "Time",
        "Duration",
        "Normal/Special Seat",
        "Price",
    ]

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gd.build()

    # If date is not none, set it as title
    # 20230202 -> 2023-02-02
    date = st.session_state.search_date
    if date is not None:
        date_formatted = date[:4] + "/" + date[4:6] + "/" + date[6:]
        st.write("Search results for {}:".format(date_formatted))

    grid_return = AgGrid(
        df,
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

    new_df = pd.DataFrame(grid_return["selected_rows"])

    # get train_codes from new df
    if not new_df.empty:
        train_codes = new_df["No"].tolist()
        # st.write(train_codes)

    st.header("Runner Settings")
    st.write(
        "The app will automatically reserve and/or notify you when the train is available."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Reserve settings")
        st.write(
            f"Reserve the train(s) automatically. You will need to reserve in the app/website within few minutes here: {LINKS[mode]['reserve_link']}"
        )
        st.write(
            "If you do not process the payment, the reservation will be cancelled automatically."
        )
        st.number_input(
            "Number of tickets",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
            key="num_tickets",
        )
    with col2:
        st.subheader("Email notifications settings")
        st.write("Notify you when the train is available.")
        st.write(
            "Receivers are the email addresses that will receive notifications. Use commas to separate multiple addresses."
        )
        st.write(
            "Note: sender email is k-trains@gmail.com. Be sure to check your spam folder."
        )
        email_receivers = st.text_input("Receivers", st.session_state.email_receivers)
        st.session_state.email_receivers = email_receivers

    col1, col2 = st.columns(2)
    col1.checkbox("Reserve", key="reserve", value=True)
    col2.checkbox("Notify", key="notify", value=True)

    st.markdown("---")

    if st.button("Submit"):

        if email_receivers == "" and st.session_state.notify:
            st.error("Please set receiver(s) email in the sidebar")
        elif new_df.empty:
            st.error("Please select at least one train")
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
                dep,
                "--arr",
                arr,
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
            ]
            print(" ".join(command))
            pid = subprocess.Popen(command)  # open in background
            st.session_state.running = True
            st.session_state.pid = pid
            save_to_log("")  # clear log
            st.write("Running...")

# If running, show log
if st.session_state.running:
    st.write(
        "Hang tight, I'm running... This may take some time, until we find a train!"
    )
    st.markdown("---")
    st.write("Log:")
    with open("log.txt", "r") as f:
        log = f.read()
        if st.session_state.previous_log != log:
            st.session_state.previous_log = log
            st.write(log)

    # Stop runner
    st.markdown("---")
    if st.button("Stop runner"):
        if st.session_state.pid is not None:
            st.session_state.pid.terminate()
            st.success("Stopped")
            st.session_state.running = False
        else:
            st.error("No process running")
