import requests
import datetime
import json
from datetime import timedelta, timezone
from functools import reduce



from src.korail.constants import *
from src.korail.errors import *
from src.korail.train import TrainType, Train, Ticket, Reservation, ReserveOption
from src.korail.utils import _get_utf8
from src.korail.passenger import *



# noinspection PyUnresolvedReferences,PyRedeclaration
class Korail(object):
    """Korail object"""
    _session = requests.session()

    _device = 'AD'
    _version = '190617001'
    _key = 'korail1234567890'

    membership_number = None
    name = None
    email = None

    def __init__(self, korail_id, korail_pw, auto_login=True, want_feedback=False):
        self._session.headers.update({'User-Agent': DEFAULT_USER_AGENT})
        self.korail_id = korail_id
        self.korail_pw = korail_pw
        self.want_feedback = want_feedback
        self.logined = False
        if auto_login:
            self.login(korail_id, korail_pw)

    def login(self, korail_id=None, korail_pw=None):
        """Login to Korail server.
:param korail_id : `Korail membership number` or `phone number` or `email`
    membership   : xxxxxxxx (8 digits)
    phone number : xxx-xxxx-xxxx
    email        : xxx@xxx.xxx
:param korail_pw : Korail account korail_pw
:param auto_login=True :

First, you need to create a Korail object.

    >>> from korail2 import *
    >>> korail = Korail("12345678", YOUR_PASSWORD) # with membership number
    >>> korail = Korail("carpedm20@gmail.com", YOUR_PASSWORD) # with email
    >>> korail = Korail("010-9964-xxxx", YOUR_PASSWORD) # with phone number

If you do not want login automatically,

    >>> korail = Korail("12345678", YOUR_PASSWORD, auto_login=False)
    >>> korail.login()
    True

When you want change ID using existing object,

    >>> korail.login(ANOTHER_ID, ANOTHER_PASSWORD)
    True

"""
        if korail_id is None:
            korail_id = self.korail_id
        else:
            self.korail_id = korail_id

        if korail_pw is None:
            korail_pw = self.korail_pw
        else:
            self.korail_pw = korail_pw

        if EMAIL_REGEX.match(korail_id):
            txt_input_flg = '5'
        elif PHONE_NUMBER_REGEX.match(korail_id):
            txt_input_flg = '4'
        else:
            txt_input_flg = '2'

        url = KORAIL_LOGIN
        data = {
            'Device': self._device,
            'Version': '150718001', # HACK
            #'Version': self._version,
            # 2 : for membership number,
            # 4 : for phone number,
            # 5 : for email,
            'txtInputFlg': txt_input_flg,
            'txtMemberNo': korail_id,
            'txtPwd': korail_pw
        }

        r = self._session.post(url, data=data)
        j = json.loads(r.text)

        if j['strResult'] == 'SUCC' and j.get('strMbCrdNo') is not None:
            self._key = j['Key']
            self.membership_number = j['strMbCrdNo']
            self.name = j['strCustNm']
            self.email = j['strEmailAdr']
            self.logined = True
            return True
        else:
            self.logined = False
            return False

    def logout(self):
        """Logout from Korail server"""
        url = KORAIL_LOGOUT
        self._session.get(url)
        self.logined = False

    def _result_check(self, j):
        """Result data check"""
        if self.want_feedback:
            print(j['h_msg_txt'])

        if j['strResult'] == 'FAIL':
            h_msg_cd = _get_utf8(j, 'h_msg_cd')
            h_msg_txt = _get_utf8(j, 'h_msg_txt')
            # P058 : 로그인 필요
            matched_error = list(filter(lambda x: h_msg_cd in x, (NoResultsError, NeedToLoginError, SoldOutError)))
            if matched_error:
                raise matched_error[0](h_msg_cd)
            else:
                raise KorailError(h_msg_txt, h_msg_cd)
        else:
            return True

    def search_train_allday(self, dep, arr, date=None, time=None, train_type=TrainType.ALL,
                            passengers=None, include_no_seats=False):
        """Search all trains for specific time and date."""
        min1 = timedelta(minutes=1)
        all_trains = []
        last_time = time
        for i in range(15):  # 최대 15번 호출
            try:
                trains = self.search_train(dep, arr, date, last_time, train_type, passengers, True)
                all_trains.extend(trains)
                # 마지막 열차시간에 1분 더해서 계속 검색.
                t = datetime.strptime(all_trains[-1].dep_time, "%H%M%S") + min1
                last_time = t.strftime("%H%M%S")
            except NoResultsError:
                break

        if not include_no_seats:
            all_trains = list(filter(lambda x: x.has_seat(), all_trains))

        if len(all_trains) == 0:
            raise NoResultsError()

        return all_trains

    def search_train(self, dep, arr, date=None, time=None, train_type=TrainType.ALL,
                     passengers=None, include_no_seats=False):
        """Search trains for specific time and date.

:param dep: A departure station in Korean  ex) '서울'
:param arr: A arrival station in Korean  ex) '부산'
:param date: (optional) A departure date in `yyyyMMdd` format
:param time: (optional) A departure time in `hhmmss` format
:param train_type: (optional) A type of train
                   - 00: KTX, KTX-산천
                   - 01: 새마을호
                   - 02: 무궁화호
                   - 03: 통근열차
                   - 04: 누리로
                   - 05: 전체 (기본값)
                   - 06: 공학직통
                   - 07: KTX-산천
                   - 08: ITX-새마을
                   - 09: ITX-청춘
:param passengers=None: (optional) List of Passenger Objects. None means 1 AdultPassenger.
:param include_no_seats=False: (optional) When True, a result includes trains which has no seats.

Below is a sample usage of `search_train`:

    >>> dep = '서울'
    >>> arr = '동대구'
    >>> date = '20140815'
    >>> time = '144000'
    >>> trains = korail.search_train(dep, arr, date, time)
    [[KTX] 8월 3일, 서울~부산(11:00~13:42) 특실,일반실 예약가능,
     [ITX-새마을] 8월 3일, 서울~부산(11:04~16:00) 일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(12:00~14:43) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(12:30~15:13) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(12:40~15:45) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(12:55~15:26) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(13:00~15:37) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(13:10~15:58) 특실,일반실 예약가능]

When you want to see trains which has no seats.

    >>> trains = korail.search_train(dep, arr, date, time, include_no_seats=True)
    [[KTX] 8월 3일, 서울~부산(11:00~13:42) 특실,일반실 예약가능,
     [ITX-새마을] 8월 3일, 서울~부산(11:04~16:00) 일반실 예약가능,
     [무궁화호] 8월 3일, 서울~부산(11:08~16:54) 입석 역발매중,
     [ITX-새마을] 8월 3일, 서울~부산(11:50~16:50) 입석 역발매중,
     [KTX] 8월 3일, 서울~부산(12:00~14:43) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(12:30~15:13) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(12:40~15:45) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(12:55~15:26) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(13:00~15:37) 특실,일반실 예약가능,
     [KTX] 8월 3일, 서울~부산(13:10~15:58) 특실,일반실 예약가능]

`passengers` is a list(or tuple) of Passeger Objects.
By this, you can search for multiple passengers.
There are 4 types of Passengers now, AdultPassenger, ChildPassenger, ToddlerPassenger and SeniorPassenger.

    # for 1 adult, 1 child, 1 toddler
    >>> psgrs = [AdultPassenger(), ChildPassenger(), ToddlerPassenger()]

    # for 2 adults, 1 child
    >>> psgrs = [AdultPassenger(2), ChildPassenger(1)]
    # ditto. They are being added each other by same group.
    >>> psgrs = [AdultPassenger(), AdultPassenger(), ChildPassenger()]

    # for 2 adults, 1 child, 1 senior
    >>> psgrs = [AdultPassenger(2), ChildPassenger(), SeniorPassenger()]

    # for 1 adult, It supports negative count or zero count.
    # But it uses passengers which the sum is greater than zero.
    >>> psgrs = [AdultPassenger(2), AdultPassenger(-1)]
    >>> psgrs = [AdultPassenger(), SeniorPassenger(0)]

    # Nothing
    >>> psgrs = [AdultPassenger(0), SeniorPassenger(0)]

    # then search or reserve train
    >>> trains = korail.search_train(dep, arr, date, time, passengers=psgrs)
    ...
    >>> korail.reserve(trains[0], psgrs)
    ...

"""
        # NOTE: 버그 수정. 코레일에 열차 티켓 리스트 API 요청시 한국시간을 기준으로 함.
        kst = timezone(timedelta(hours=9))
        if date is None:
            date = datetime.utcnow().astimezone(kst).strftime("%Y%m%d")
        if time is None:
            time = datetime.utcnow().astimezone(kst).strftime("%H%M%S")

        if passengers is None:
            passengers = [AdultPassenger()]

        passengers = Passenger.reduce(passengers)

        adult_count = reduce(lambda a, b: a + b.count, list(filter(lambda x: isinstance(x, AdultPassenger), passengers)), 0)
        child_count = reduce(lambda a, b: a + b.count, list(filter(lambda x: isinstance(x, ChildPassenger), passengers)), 0)
        toddler_count = reduce(lambda a, b: a + b.count, list(filter(lambda x: isinstance(x, ToddlerPassenger), passengers)), 0)
        senior_count = reduce(lambda a, b: a + b.count, list(filter(lambda x: isinstance(x, SeniorPassenger), passengers)), 0)

        url = KORAIL_SEARCH_SCHEDULE
        data = {
            'Device': self._device,
            'radJobId': '1',
            'selGoTrain': train_type,
            'txtCardPsgCnt': '0',
            'txtGdNo': '',
            'txtGoAbrdDt': date,  # '20140803',
            'txtGoEnd': arr,
            'txtGoHour': time,  # '071500',
            'txtGoStart': dep,
            'txtJobDv': '',
            'txtMenuId': '11',
            'txtPsgFlg_1': adult_count,  # 어른
            'txtPsgFlg_2': child_count,  # 어린이
            'txtPsgFlg_8': toddler_count,  # 유아
            'txtPsgFlg_3': senior_count,  # 경로
            'txtPsgFlg_4': '0',  # 중증 장애인
            'txtPsgFlg_5': '0',  # 경증 장애인
            'txtSeatAttCd_2': '000',
            'txtSeatAttCd_3': '000',
            'txtSeatAttCd_4': '015',
            'txtTrnGpCd': train_type,

            'Version': self._version,
        }


        r = self._session.get(url, params=data)
        j = json.loads(r.text)

        if self._result_check(j):
            train_infos = j['trn_infos']['trn_info']

            trains = []

            for info in train_infos:
                trains.append(Train(info))

            if not include_no_seats:
                trains = list(filter(lambda x: x.has_seat(), trains))

            if len(trains) == 0:
                raise NoResultsError()

            return trains

    def reserve(self, train, passengers=None, option=ReserveOption.GENERAL_FIRST):
        """Reserve a train.

:param train: An instance of `Train`.
:param passengers=None: (optional) List of Passenger Objects. None means 1 AdultPassenger.
:param option=ReserveOption.GENERAL_FIRST : (optional)

When tickets are not enough much for passengers, it raises SoldOutError.

If you want to select priority of seat grade, general or special,
There are 4 options in ReserveOption class.

- GENERAL_FIRST : Economic than Comfortable.
- GENERAL_ONLY  : Reserve only general seats. You are poorman ;-)
- SPECIAL_FIRST : Comfortable than Economic.
- SPECIAL_ONLY  : Richman.

        """

        # 좌석 선택 옵션에 따라 결정.
        seat_type = None
        if train.has_seat() is False:  # 자리가 둘다 없는 경우는 SoldOutError발생
            raise SoldOutError()
        elif option == ReserveOption.GENERAL_ONLY:  # 이후 일반석, 특실 중 하나는 무조건 있는 조건
            if train.has_general_seat():
                seat_type = '1'
            else:
                raise SoldOutError()
        elif option == ReserveOption.SPECIAL_ONLY:
            if train.has_special_seat():
                seat_type = '2'
            else:
                raise SoldOutError()
        elif option == ReserveOption.GENERAL_FIRST:
            if train.has_general_seat():
                seat_type = '1'
            else:
                seat_type = '2'
        elif option == ReserveOption.SPECIAL_FIRST:
            if train.has_special_seat():
                seat_type = '2'
            else:
                seat_type = '1'

        if passengers is None:
            passengers = [AdultPassenger()]

        print(train)

        passengers = Passenger.reduce(passengers)
        cnt = reduce(lambda x,y: x + y.count, passengers, 0)
        url = KORAIL_TICKETRESERVATION
        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'txtGdNo': '',
            'txtJobId': '1101',
            'txtTotPsgCnt': cnt,
            'txtSeatAttCd1': '000',
            'txtSeatAttCd2': '000',
            'txtSeatAttCd3': '000',
            'txtSeatAttCd4': '015',
            'txtSeatAttCd5': '000',
            'hidFreeFlg': 'N',
            'txtStndFlg': 'N',
            'txtMenuId': '11',
            'txtSrcarCnt': '0',
            'txtJrnyCnt': '1',

            # 이하 여정정보1
            'txtJrnySqno1': '001',
            'txtJrnyTpCd1': '11',
            'txtDptDt1': train.dep_date,
            'txtDptRsStnCd1': train.dep_code,
            'txtDptTm1': train.dep_time,
            'txtArvRsStnCd1': train.arr_code,
            'txtTrnNo1': train.train_no,
            'txtRunDt1': train.run_date,
            'txtTrnClsfCd1': train.train_type,
            'txtPsrmClCd1': seat_type,
            'txtTrnGpCd1': train.train_group,
            'txtChgFlg1': '',

            # 이하 여정정보2
            'txtJrnySqno2': '',
            'txtJrnyTpCd2': '',
            'txtDptDt2': '',
            'txtDptRsStnCd2': '',
            'txtDptTm2': '',
            'txtArvRsStnCd2': '',
            'txtTrnNo2': '',
            'txtRunDt2': '',
            'txtTrnClsfCd2': '',
            'txtPsrmClCd2': '',
            'txtChgFlg2': '',

            # 이하 txtTotPsgCnt 만큼 반복
            # 'txtPsgTpCd1'    : '1',   #손님 종류 (어른, 어린이)
            # 'txtDiscKndCd1'  : '000', #할인 타입 (경로, 동반유아, 군장병 등..)
            # 'txtCompaCnt1'   : '1',   #인원수
            # 'txtCardCode_1'  : '',
            # 'txtCardNo_1'    : '',
            # 'txtCardPw_1'    : '',
        }

        index = 1
        for psg in passengers:
            data.update(psg.get_dict(index))
            index += 1

        r = self._session.get(url, params=data)
        j = json.loads(r.text)
        if self._result_check(j):
            rsv_id = j['h_pnr_no']
            rsvlist = list(filter(lambda x: x.rsv_id == rsv_id, self.reservations()))
            if len(rsvlist) == 1:
                return rsvlist[0]

    def tickets(self):
        """Get list of tickets"""
        url = KORAIL_MYTICKETLIST
        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'txtIndex': '1',
            'h_page_no': '1',
            'txtDeviceId': '',
            'h_abrd_dt_from': '',
            'h_abrd_dt_to': '',
        }

        r = self._session.get(url, params=data)
        j = json.loads(r.text)
        try:
            if self._result_check(j):
                ticket_infos = j['reservation_list']

                tickets = []

                for info in ticket_infos:
                    ticket = Ticket(info)
                    url = KORAIL_MYTICKET_SEAT
                    data = {
                        'Device': self._device,
                        'Version': self._version,
                        'Key': self._key,
                        'h_orgtk_wct_no': ticket.sale_info1,
                        'h_orgtk_ret_sale_dt': ticket.sale_info2,
                        'h_orgtk_sale_sqno': ticket.sale_info3,
                        'h_orgtk_ret_pwd': ticket.sale_info4,
                    }
                    r = self._session.get(url, params=data)
                    j = json.loads(r.text)
                    if self._result_check(j):
                        seat = j['ticket_infos']['ticket_info'][0]['tk_seat_info'][0]
                        ticket.seat_no = _get_utf8(seat, 'h_seat_no')
                        ticket.seat_no_end = None

                    tickets.append(ticket)

                return tickets
        except NoResultsError:
            return []

    def reservations(self):
        """ Get My Reservations """
        url = KORAIL_MYRESERVATIONLIST
        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
        }
        r = self._session.get(url, params=data)
        j = json.loads(r.text)
        try:
            if self._result_check(j):
                rsv_infos = j['jrny_infos']['jrny_info']

                reserves = []

                for info in rsv_infos:
                    for tinfo in info['train_infos']['train_info']:
                        reserves.append(Reservation(tinfo))
                return reserves
        except NoResultsError:
            return []

    def cancel(self, rsv):
        """ Cancel Reservation : Canceling is for reservation, for ticket would be Refunding """
        assert isinstance(rsv, Reservation)
        url = KORAIL_CANCEL
        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'txtPnrNo': rsv.rsv_id,
            'txtJrnySqno': rsv.journey_no,
            'txtJrnyCnt': rsv.journey_cnt,
            'hidRsvChgNo': rsv.rsv_chg_no,
        }
        r = self._session.get(url, data=data)
        j = json.loads(r.text)
        if self._result_check(j):
            return True
