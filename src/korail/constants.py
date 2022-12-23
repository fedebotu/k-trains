__author__ = 'sng2c'

import re

class EnumItem(str):
    """EnumItem : str상속, desc로 상세설명조회"""

    def __init__(self, code):
        super(EnumItem, self).__init__(code)
        self.desc = None


class Enum:
    def __init__(self, kv):
        assert isinstance(kv, dict)
        self.kv = {}
        for k, v in kv.items():
            self.kv[k] = EnumItem(k)
            self.kv[k].desc = v

    def __getitem__(self, key):
        """조회해서 있으면 EnumItem을 출력하고 없으면 key를 그대로 리턴"""
        return self.kv.get(str(key), key)


enum_h_jrny_tp_cd = Enum(
    {
        10: "열차상품",
        11: "편도",
        12: "왕편",
        13: "복편",
        14: "환승편도",
        15: "왕편환승",
        16: "복편환승",
        20: "병합",
        21: "병합선행",
        22: "병합후행",
        50: "열차외상품",
        51: "숙박",
        52: "렌터카",
        53: "선박",
        54: "이벤트",
        55: "항공",
    })

enum_h_psg_tp_cd = Enum(
    {
        1: "어른",
        2: "unknown",
        3: "어린이",
    })

enum_h_psrm_cl_cd = Enum(
    {
        1: "일반실",
        2: "특실",
        3: "침대실",
        4: "가족실",
        5: "별실",
        6: "비승용",
        7: "우등실",
    })

enum_h_rsv_tp_cd = Enum(
    {
        0: "unknown",
        1: "특단",
        2: "전세",
        3: "일반",
        4: "대납",
        5: "Open",
        6: "T-Less",
        7: "OVER",
        8: "대기",
        9: "단체",
        10: "열전",
        11: "군수송",
        12: "우편배송",
    })

enum_h_seat_att_cd_2 = Enum(
    {
        9: "순방",
        10: "역방",
    })

enum_h_seat_att_cd_3 = Enum(
    {
        11: "1인",
        12: "창측",
        13: "내측",
    })

enum_h_trn_clsf_cd = Enum(
    {
        "00": "KTX, KTX-산천",
        "01": "새마을호",
        "02": "무궁화호",
        "03": "통근열차",
        "04": "누리로",
        "05": "전체",
        "06": "공학직통",
        "KTX-07": "KTX-산천",
        "ITX-08": "ITX-새마을",
        "ITX-09": "ITX-청춘",
    })
    

class TrainType:
    KTX = "100"  # "KTX, KTX-산천",
    SAEMAEUL = "101"  # "새마을호",
    MUGUNGHWA = "102"  # "무궁화호",
    TONGGUEN = "103"  # "통근열차",
    NURIRO = "102"  # "누리로",
    ALL = "109"  # "전체",
    AIRPORT = "105"  # "공항직통",
    KTX_SANCHEON = "100"  # "KTX-산천",
    ITX_SAEMAEUL = "101"  # "ITX-새마을",
    ITX_CHEONGCHUN = "104"  # "ITX-청춘",

    def __init__(self):
        raise NotImplementedError("Do not make instance.")
    
    
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_NUMBER_REGEX = re.compile(r"(\d{3})-(\d{3,4})-(\d{4})")

SCHEME = "https"
KORAIL_HOST = "smart.letskorail.com"
KORAIL_PORT = "443"

KORAIL_DOMAIN = "%s://%s:%s" % (SCHEME, KORAIL_HOST, KORAIL_PORT)
KORAIL_MOBILE = "%s/classes/com.korail.mobile" % KORAIL_DOMAIN

KORAIL_LOGIN = "%s.login.Login" % KORAIL_MOBILE
KORAIL_LOGOUT = "%s.common.logout" % KORAIL_MOBILE
KORAIL_SEARCH_SCHEDULE = "%s.seatMovie.ScheduleView" % KORAIL_MOBILE
KORAIL_TICKETRESERVATION = "%s.certification.TicketReservation" % KORAIL_MOBILE
KORAIL_REFUND = "%s.refunds.RefundsRequest" % KORAIL_MOBILE
KORAIL_MYTICKETLIST = "%s.myTicket.MyTicketList" % KORAIL_MOBILE
KORAIL_MYTICKET_SEAT = "%s.refunds.SelTicketInfo" % KORAIL_MOBILE

KORAIL_MYRESERVATIONLIST = "%s.reservation.ReservationView" % KORAIL_MOBILE
KORAIL_CANCEL = "%s.reservationCancel.ReservationCancelChk" % KORAIL_MOBILE

KORAIL_STATION_DB = "%s.common.stationinfo?device=ip" % KORAIL_MOBILE
KORAIL_STATION_DB_DATA = "%s.common.stationdata" % KORAIL_MOBILE
KORAIL_EVENT = "%s.common.event" % KORAIL_MOBILE
KORAIL_PAYMENT = "%s/ebizmw/PrdPkgMainList.do" % KORAIL_DOMAIN
KORAIL_PAYMENT_VOUCHER = "%s/ebizmw/PrdPkgBoucherView.do" % KORAIL_DOMAIN

DEFAULT_USER_AGENT = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 4 Build/LMY48T)"

