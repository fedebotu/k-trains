def _get_utf8(data, key, default=None):
    v = data.get(key, default)

    return v


class ExceptionForm(type):
    codes = set()

    def __contains__(cls, item):
        return item in cls.codes
