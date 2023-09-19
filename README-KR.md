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

> English version [here](README.md)

_SRT가 예약이 가득 차서 수서역으로 티켓이 없으신가요? 아니면 이미 매진된 저렴한 무궁화 티켓 때문에 고민하고 계신가요? K-Trains가 도와드리겠습니다!_

K-Trains는 [Korail](https://www.letskorail.com/)과 [SRT](https://etk.srail.kr/)의 API에 연결하여 한국의 기차 정보를 얻고 예약하는 Streamlit 앱입니다.



## 사용 방법

### 웹 UI
Streamlit에서 앱을 실행하려면 [여기](https://k-trains.streamlit.app/)를 클릭하세요. UI는 자기 설명적이므로 로그인하고 알림을 받거나 직접 예약하고 싶은 기차를 선택하기만 하면 됩니다. 가능하지 않다면 앱이 사용 가능할 때 알려주고 당신을 위해 예약합니다!

_티켓에 대한 비용은 Korail 또는 SRT 웹사이트/앱에서 시간 내에 지불해야 합니다._

그럼에도 불구하고 수동으로 새로 고침하고 누군가가 티켓을 먼저 예약하지 않을 것이라고 기대하는 것보다는 나을 것입니다 ;)

### 수동 배포

이 응용 프로그램은 Python에서 웹 GUI를 허용하는 [Streamlit](https://streamlit.io/)를 기반으로 합니다. 로컬에서 애플리케이션을 실행하려면 다음 명령을 실행하세요:

```bash
streamlit run app.py
```

웹 브라우저가 자동으로 열려 애플리케이션과 상호 작용할 수 있습니다. 그렇지 않으면 브라우저를 수동으로 열고 http://localhost:8501로 이동할 수 있습니다.

또한 직접 티켓을 예약하기 위해 스크립트를 실행할 수도 있습니다:

```bash
python reserve.py [OPTIONS]
```

### 비밀 및 이메일 API 연결
앱은 이메일 계정 API(특히 Google)에 연결됩니다. 앱을 스스로 배포하려면 다음과 같은 메시지가 표시될 수 있습니다:

```bash
FileNotFoundError: No secrets files found. Valid paths for a secrets.toml file are: C:\Users\nyancat.streamlit\secrets.toml
```
자체 secrets.toml 파일을 관리하기 위해 이 가이드를 따를 수 있습니다. Gmail을 사용하지 않는 경우 email_notify 함수를 수정해야 합니다. 특히 이 줄에서입니다.

## 고지
개발자는 이 애플리케이션의 오용에 대해 책임지지 않습니다. 이 애플리케이션은 교육 목적으로만 사용됩니다. 자기 책임하에 사용하세요!

## 스크린샷
<div align="center">
<br>
<center>
<img src="https://github.com/fedebotu/k-trains/assets/48984123/55ec2078-1034-4e95-b5e2-d15de8478107" alt="k-train-email"/>
</center>
<br>
</div>


## 감사의 말
이 프로젝트는 다음 라이브러리 덕분에 가능했습니다:

Korail: https://github.com/carpedm20/korail2

SRT: https://github.com/ryanking13/SRT

### 피드백
피드백이 있다면 문제를 제기하거나 pull request를 열어주세요!