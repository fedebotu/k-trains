from src.korail.utils import _get_utf8


class Schedule(object):
    """Korail train object. Highly inspired by `korail.py
    <https://raw.githubusercontent.com/devxoul/korail/master/korail/korail.py>`_
    by `Suyeol Jeon <http://xoul.kr/>`_ at 2014.
    """

    # : 기차 종류
    # : 00: KTX
    #: 01: 새마을호
    #: 02: 무궁화호
    #: 03: 통근열차
    #: 04: 누리로
    #: 05: 전체 (검색시에만 사용)
    #: 06: 공학직통
    #: 07: KTX-산천
    #: 08: ITX-새마을
    #: 09: ITX-청춘
    train_type = None  # h_trn_clsf_cd, selGoTrain

    train_group = None # h_trn_gp_cd

    #: 기차 종류 이름
    train_type_name = None  # h_trn_clsf_nm

    #: 기차 번호
    train_no = None  # h_trn_no

    #: 출발역 이름
    dep_name = None  # h_dpt_rs_stn_nm

    #: 출발역 코드
    dep_code = None  # h_dpt_rs_stn_cd

    #: 출발 날짜 (yyyyMMdd)
    dep_date = None  # h_dpt_dt

    #: 출발 시각 (hhmmss)
    dep_time = None  # h_dpt_tm

    #: 도착역 이름
    arr_name = None  # h_arv_rs_stn_nm

    #: 도착역 코드
    arr_code = None  # h_arv_rs_stn_cd

    #: 도착 날짜 (yyyyMMdd)
    arr_date = None  # h_arv_dt

    #: 도착 시각 (hhmmss)
    arr_time = None  # h_arv_tm

    #: 운행 날짜 (yyyyMMdd)
    run_date = None  # h_run_dt


    def __init__(self, data):

        self.train_type = _get_utf8(data, 'h_trn_clsf_cd')
        self.train_type_name = _get_utf8(data, 'h_trn_clsf_nm')
        self.train_group = _get_utf8(data, 'h_trn_gp_cd')
        self.train_no = _get_utf8(data, 'h_trn_no')
        self.delay_time = _get_utf8(data, 'h_expct_dlay_hr')

        self.dep_name = _get_utf8(data, 'h_dpt_rs_stn_nm')
        self.dep_code = _get_utf8(data, 'h_dpt_rs_stn_cd')
        self.dep_date = _get_utf8(data, 'h_dpt_dt')
        self.dep_time = _get_utf8(data, 'h_dpt_tm')

        self.arr_name = _get_utf8(data, 'h_arv_rs_stn_nm')
        self.arr_code = _get_utf8(data, 'h_arv_rs_stn_cd')
        self.arr_date = _get_utf8(data, 'h_arv_dt')
        self.arr_time = _get_utf8(data, 'h_arv_tm')

        self.run_date = _get_utf8(data, 'h_run_dt')

    def __repr__(self):
        dep_time = "%s:%s" % (self.dep_time[:2], self.dep_time[2:4])
        arr_time = "%s:%s" % (self.arr_time[:2], self.arr_time[2:4])

        dep_date = "%s월 %s일" % (int(self.dep_date[4:6]), int(self.dep_date[6:]))

        repr_str = '[%s] %s, %s~%s(%s~%s)' % (
            self.train_type_name,
            dep_date,
            self.dep_name,
            self.arr_name,
            dep_time,
            arr_time,
        )

        return repr_str


class Train(Schedule):
    # : 지연 시간 (hhmm)
    delay_time = None  # h_expct_dlay_hr

    # : 예약 가능 여부
    reserve_possible = False  # h_rsv_psb_flg ('Y' or 'N')

    #: 예약 가능 여부
    reserve_possible_name = None  # h_rsv_psb_nm

    #: 특실 예약가능 여부
    #: 00: 특실 없음
    #: 11: 예약 가능
    #: 13: 매진
    special_seat = None  # h_spe_rsv_cd

    #: 일반실 예약가능 여부
    #: 00: 일반실 없음
    #: 11: 예약 가능
    #: 13: 매진
    general_seat = None  # h_gen_rsv_cd

    def __init__(self, data):
        super(Train, self).__init__(data)
        self.reserve_possible = _get_utf8(data, 'h_rsv_psb_flg')
        self.reserve_possible_name = _get_utf8(data, 'h_rsv_psb_nm')

        self.special_seat = _get_utf8(data, 'h_spe_rsv_cd')
        self.general_seat = _get_utf8(data, 'h_gen_rsv_cd')

    def __repr__(self):
        repr_str = super(Train, self).__repr__()

        if self.reserve_possible_name is not None:
            seats = []
            if self.has_special_seat():
                seats.append("특실")

            if self.has_general_seat():
                seats.append("일반실")

            repr_str += " " + (",".join(seats)) + " " + self.reserve_possible_name.replace('\n', ' ')

        return repr_str

    def has_special_seat(self):
        return self.special_seat == '11'

    def has_general_seat(self):
        return self.general_seat == '11'

    def has_seat(self):
        return self.has_general_seat() or self.has_special_seat()


class Ticket(Train):
    """Ticket object"""

    # : 열차 번호
    car_no = None  # h_srcar_no

    # : 자리 갯수
    seat_no_count = None  # h_seat_cnt  ex) 001

    #: 자리 번호
    seat_no = None  # h_seat_no

    #: 자리 번호
    seat_no_end = None  # h_seat_no_end

    #: 구매자 성함
    buyer_name = None  # h_buy_ps_nm

    #: 구매 날짜 (yyyyMMdd)
    sale_date = None  # h_orgtk_sale_dt

    #: 구매 정보1
    sale_info1 = None  # h_orgtk_wct_no

    #: 구매 정보2
    sale_info2 = None  # h_orgtk_ret_sale_dt

    #: 구매 정보3
    sale_info3 = None  # h_orgtk_sale_sqno

    #: 구매 정보4
    sale_info4 = None  # h_orgtk_ret_pwd

    #: 구매 가격
    price = None  # h_rcvd_amt  ex) 00013900

    def __init__(self, data):
        raw_data = data['ticket_list'][0]['train_info'][0]
        super(Ticket, self).__init__(raw_data)

        self.seat_no_end = _get_utf8(raw_data, 'h_seat_no_end')
        self.seat_no_count = int(_get_utf8(raw_data, 'h_seat_cnt'))

        self.buyer_name = _get_utf8(raw_data, 'h_buy_ps_nm')
        self.sale_date = _get_utf8(raw_data, 'h_orgtk_sale_dt')
        self.sale_info1 = _get_utf8(raw_data, 'h_orgtk_wct_no')
        self.sale_info2 = _get_utf8(raw_data, 'h_orgtk_ret_sale_dt')
        self.sale_info3 = _get_utf8(raw_data, 'h_orgtk_sale_sqno')
        self.sale_info4 = _get_utf8(raw_data, 'h_orgtk_ret_pwd')
        self.price = int(_get_utf8(raw_data, 'h_rcvd_amt'))

        self.car_no = _get_utf8(raw_data, 'h_srcar_no')
        self.seat_no = _get_utf8(raw_data, 'h_seat_no')

    def __repr__(self):
        repr_str = super(Train, self).__repr__()

        repr_str += " => %s호" % self.car_no

        if int(self.seat_no_count) != 1:
            repr_str += " %s~%s" % (self.seat_no, self.seat_no_end)
        else:
            repr_str += " %s" % self.seat_no

        repr_str += ", %s원" % self.price

        return repr_str

    def get_ticket_no(self):
        return "-".join(map(str, (self.sale_info1, self.sale_info2, self.sale_info3, self.sale_info4)))


class ReserveOption:
    GENERAL_FIRST = "GENERAL_FIRST"  # 일반실 우선
    GENERAL_ONLY = "GENERAL_ONLY"  # 일반실만
    SPECIAL_FIRST = "SPECIAL_FIRST"  # 특실 우선
    SPECIAL_ONLY = "SPECIAL_ONLY"  # 특실만

    def __init__(self):
        raise NotImplementedError("Do not make instance.")


class Reservation(Train):
    """Revervation object"""

    # : 예약번호
    rsv_id = None  # h_pnr_no

    # : 여정 번호
    journey_no = None  # txtJrnySqno

    #: 여정 카운트
    journey_cnt = None  # txtJrnyCnt

    #: 예약변경 번호?
    rsv_chg_no = "00000"

    #: 자리 갯수
    seat_no_count = None  # h_tot_seat_cnt  ex) 001

    #: 결제 기한 날짜
    buy_limit_date = None  # h_ntisu_lmt_dt

    #: 결제 기한 시간
    buy_limit_time = None  # h_ntisu_lmt_tm

    #: 예약 가격
    price = None  # h_rsv_amt  ex) 00013900

    #: 열차 번호 (Not implemented)
    car_no = None  # h_srcar_no

    #: 자리 번호 (Not implemented)
    seat_no = None  # h_seat_no

    #: 자리 번호 (Not implemented)
    seat_no_end = None  # h_seat_no_end

    def __init__(self, data):
        super(Reservation, self).__init__(data)
        # 이 두 필드가 결과에 빠져있음
        self.dep_date = _get_utf8(data, 'h_run_dt')
        self.arr_date = _get_utf8(data, 'h_run_dt')

        self.rsv_id = _get_utf8(data, 'h_pnr_no')
        self.seat_no_count = int(_get_utf8(data, 'h_tot_seat_cnt'))
        self.buy_limit_date = _get_utf8(data, 'h_ntisu_lmt_dt')
        self.buy_limit_time = _get_utf8(data, 'h_ntisu_lmt_tm')
        self.price = int(_get_utf8(data, 'h_rsv_amt'))
        self.journey_no = _get_utf8(data, 'txtJrnySqno', "001")
        self.journey_cnt = _get_utf8(data, 'txtJrnyCnt', "01")
        self.rsv_chg_no = _get_utf8(data, 'hidRsvChgNo', "00000")


        # 좌석정보 추가 업데이트 필요.
        # self.car_no = None
        # self.seat_no = None
        # self.seat_no_end = None



    def __repr__(self):
        repr_str = super(Reservation, self).__repr__()

        repr_str += ", %s원(%s석)" % (self.price, self.seat_no_count)

        buy_limit_time = "%s:%s" % (self.buy_limit_time[:2], self.buy_limit_time[2:4])

        buy_limit_date = "%s월 %s일" % (int(self.buy_limit_date[4:6]), int(self.buy_limit_date[6:]))

        repr_str += ", 구입기한 %s %s" % (buy_limit_date, buy_limit_time)

        return repr_str

        