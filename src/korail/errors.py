
class KorailError(with_metaclass(ExceptionForm, Exception)):
    """Korail Base Error Class"""

    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

    def __str__(self):
        return "%s (%s)" % (self.msg, self.code)


class NeedToLoginError(KorailError):
    """Korail NeedToLogin Error Class"""
    codes = {'P058'}

    def __init__(self, code=None):
        KorailError.__init__(self, "Need to Login", code)


class NoResultsError(KorailError):
    """Korail NoResults Error Class"""
    codes = {'P100',
             'WRG000000',
             'WRD000061',  # 직통열차는 없지만, 환승으로 조회 가능합니다.
             'WRT300005'
    }

    def __init__(self, code=None):
        KorailError.__init__(self, "No Results", code)


class SoldOutError(KorailError):
    codes = {'ERR211161'}

    def __init__(self, code=None):
        KorailError.__init__(self, "Sold out", code)
