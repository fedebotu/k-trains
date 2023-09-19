<div align="center">

# K-Trains 🇰🇷-🚄


 [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_red.svg)](https://k-trains.streamlit.app)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![python_sup](https://img.shields.io/badge/python-3.7+-blue.svg?)](https://www.python.org/downloads/release/python-370/)

<br>
<center>
<img src="assets/ktrains.png" alt="K-Trains" width="300"/>
</center>
<br>
<br>
 </div>

> 한국어 버전 [클릭](README-KR.md)


_Tired of not having any ticket to Suseo station because your SRT is fully booked? How about that cheap Mugunghwa ticket that you can't get because it's sold out? K-Trains is here to help you get those tickets!_


K-Trains is a Streamlit app that allows you to connect to [Korail](https://www.letskorail.com/) and [SRT](https://etk.srail.kr/)'s APIs to get information and reserve trains in Korea.

## How to use

### Web UI
You can launch the app on Streamlit [here](https://k-trains.streamlit.app/). The UI should be self-explanatory - you can simply login and pick up some trains that you would like to get notifications for or reserve them directly. If they are not available, the app will notify you when they are and reserve them for you! 

_Note that you still have to pay for the ticket in the Korail or SRT website/app within the time limit_.

Nonetheless, still better than having to manually refresh and hope someone won't reserve the ticket before you do ;)

### Manual deployment

The application is based on [Streamlit](https://streamlit.io/) which allows for web GUIs in Python. To run the application locally, run the following command:

```bash
streamlit run app.py
```

A web browser should open automatically and you can interact with the application. If it doesn't, you can manually open a browser and navigate to http://localhost:8501.

You can also run the script to book a ticket directly:

```bash
python reserve.py [OPTIONS]
```

### Secrets and email API connection
The app connects to a email account API (specifically, Google), which is private. If you want to deploy the app by yourself, you may encounter the following:
```bash
FileNotFoundError: No secrets files found. Valid paths for a secrets.toml file are: C:\Users\nyancat.streamlit\secrets.toml,
```
You may follow [this guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management) for managing your own `secrets.toml` file. Moreover, if you do not use Gmail, you should modify the `email_notify` function, particularly at [this line](https://github.com/fedebotu/k-trains/blob/1a1f609600f870f09e3ef8fe4e692cc082fdb3cc/ktrains/notify.py#L49C1-L50C1).

## Disclaimer 
Developers are not responsible for any misuse of this application. This application is for educational purposes only. Please use it at your own risk!

## Screenshots

<div align="center">
<br>
<center>
<img src="https://github.com/fedebotu/k-trains/assets/48984123/55ec2078-1034-4e95-b5e2-d15de8478107" alt="k-train-email"/>
</center>
<br>
 </div>
 

## Acknowledgements

This project was made possible by the following libraries:

- Korail: https://github.com/carpedm20/korail2
- SRT: https://github.com/ryanking13/SRT


## Feedback
If you have any feedback, please feel free to reach out and open an issue or a pull request!
