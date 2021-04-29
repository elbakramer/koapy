from functools import wraps


class CybosPlusError(Exception):

    pass


class CybosPlusRequestError(CybosPlusError):

    """
    아래 문서에서 [BlockRequest/Blockrequest2/Request의 리턴값] 내용 참조
    http://cybosplus.github.io/cputil_rtf_1_/cybosplus_interface.htm
    """

    ERROR_MESSAGE_BY_CODE = {
        0: "정상요청",
        1: "통신요청 실패",
        2: "주문확인창에서 취소",
        3: "그외의 내부 오류",
        4: "주문요청 제한 개수 초과",
    }

    @classmethod
    def get_error_message_by_code(cls, code, default=None):
        return cls.ERROR_MESSAGE_BY_CODE.get(code, default)

    @classmethod
    def check_code_or_raise(cls, code):
        if code != 0:
            raise cls(code)
        return code

    @classmethod
    def wrap_to_check_code_or_raise(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cls.check_code_or_raise(func(*args, **kwargs))

        return wrapper

    @classmethod
    def try_or_raise(cls, arg):
        if isinstance(arg, int):
            return cls.check_code_or_raise(arg)
        elif callable(arg):
            return cls.wrap_to_check_code_or_raise(arg)
        else:
            raise TypeError("Expected 'int' or 'callable' but %s found" % type(arg))

    def __init__(self, code, message=None):
        if message is None:
            message = self.get_error_message_by_code(code)

        super().__init__(message)

        self._code = code
        self._message = message

    def __str__(self):
        return self._message

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self._code, self._message)

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message
