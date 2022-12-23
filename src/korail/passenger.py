import itertools
from functools import reduce


class Passenger:
    """승객. Passenger List를 검색과 예약에 쓰도록 한다."""
    typecode = None  # txtPsgTpCd1    : '1',   #손님 종류 (어른 1, 어린이 3)
    discount_type = '000'  # txtDiscKndCd1  : '000', #할인 타입 (경로, 동반유아, 군장병 등..)
    count = 1  # txtCompaCnt1   : '1',   #인원수
    card = ''  # txtCardCode_1  : '',    #할인카드 종류
    card_no = ''  # txtCardNo_1    : '',    #할인카드 번호
    card_pw = ''  # txtCardPw_1    : '',    #할인카드 비밀번호

    @staticmethod
    def reduce(passenger_list):
        """Reduce passenger's list."""
        if list(filter(lambda x: not isinstance(x, Passenger), passenger_list)):
            raise TypeError("Passengers must be based on Passenger")

        groups = itertools.groupby(passenger_list, lambda x: x.group_key())
        return list(filter(lambda x: x.count > 0, [reduce(lambda a, b: a + b, g) for k, g in groups]))

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Passenger is abstract class. Do not make instance.")

    def __init_internal__(self, typecode, count=1, discount_type='000', card='', card_no='', card_pw=''):
        self.typecode = typecode
        self.count = count
        self.discount_type = discount_type
        self.card = card
        self.card_no = card_no
        self.card_pw = card_pw

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        if self.group_key() == other.group_key():
            return self.__class__(count=self.count + other.count, discount_type=self.discount_type, card=self.card,
                                  card_no=self.card_no, card_pw=self.card_pw)
        else:
            raise TypeError(
                "other's group_key(%s) is not equal to self's group_key(%s)." % (other.group_key(), self.group_key()))

    def group_key(self):
        """get group string from attributes except count"""
        return "%s_%s_%s_%s_%s" % (self.typecode, self.discount_type, self.card, self.card_no, self.card_pw)

    def get_dict(self, index):
        assert isinstance(index, int)
        index = str(index)
        return {
            'txtPsgTpCd' + index: self.typecode,
            'txtDiscKndCd' + index: self.discount_type,
            'txtCompaCnt' + index: self.count,
            'txtCardCode_' + index: self.card,
            'txtCardNo_' + index: self.card_no,
            'txtCardPw_' + index: self.card_pw,
        }


# noinspection PyMissingConstructor
class AdultPassenger(Passenger):
    def __init__(self, count=1, discount_type='000', card='', card_no='', card_pw=''):
        Passenger.__init_internal__(self, '1', count, discount_type, card, card_no, card_pw)


# noinspection PyMissingConstructor
class ChildPassenger(Passenger):
    def __init__(self, count=1, discount_type='000', card='', card_no='', card_pw=''):
        Passenger.__init_internal__(self, '3', count, discount_type, card, card_no, card_pw)


# noinspection PyMissingConstructor
class ToddlerPassenger(Passenger):
    def __init__(self, count=1, discount_type='321', card='', card_no='', card_pw=''):
        Passenger.__init_internal__(self, '3', count, discount_type, card, card_no, card_pw)


# noinspection PyMissingConstructor
class SeniorPassenger(Passenger):
    def __init__(self, count=1, discount_type='131', card='', card_no='', card_pw=''):
        Passenger.__init_internal__(self, '1', count, discount_type, card, card_no, card_pw)

