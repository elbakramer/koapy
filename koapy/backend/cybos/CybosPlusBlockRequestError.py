class CybosPlusBlockRequestError(Exception):

    ERROR_MESSAGE_BY_CODE = {
        0: '정상요청',
        1: '통신요청 실패',
        2: '주문확인창에서 취소',
        3: '그외의 내부 오류',
        4: '주문요청 제한 개수 초과',
    }

    @classmethod
    def get_error_message_by_code(cls, code):
        return cls.ERROR_MESSAGE_BY_CODE.get(code)

    @classmethod
    def try_or_raise(cls, code_or_function, *args, **kwargs):
        if callable(code_or_function):
            code = code_or_function(*args, **kwargs)
        elif isinstance(code_or_function, int):
            code = code_or_function
        else:
            raise ValueError('Invalid argument for code_or_function: %s' % code_or_function)
        if code != 0:
            raise cls(code)
        return code

    def __init__(self, code, message=None):
        if message is None:
            message = self.get_error_message_by_code(code)

        self._code = code
        self._message = message

        super().__init__(self._message)

    def __str__(self):
        return self._message

    def __repr__(self):
        return '%s(%d, %r)' % (self.__class__.__name__, self._code, self._message)
