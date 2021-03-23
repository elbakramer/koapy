from functools import wraps

class KiwoomOpenApiWError(Exception):

    def __init__(self, message=None):
        if message is not None:
            super().__init__(message)
        else:
            super().__init__()

        self._message = message

    @property
    def message(self):
        return self._message

    @classmethod
    def try_or_raise(cls, arg, message=None):
        return KiwoomOpenApiWNegativeReturnCodeError.try_or_raise(arg, message)

    @classmethod
    def try_or_raise_boolean(cls, arg, message):
        return KiwoomOpenApiWBooleanReturnCodeError.try_or_raise(arg, message)

class KiwoomOpenApiWNegativeReturnCodeError(KiwoomOpenApiWError):

    OP_ERR_NONE = 0
    OP_ERR_NO_LOGIN = -1
    OP_ERR_LOGIN = -100
    OP_ERR_CONNECT = -101
    OP_ERR_VERSION = -102
    OP_ERR_TRCODE = -103
    OP_ERR_NO_REGOPENAPI = -104
    OP_ERR_SISE_OVERFLOW = -200
    OP_ERR_ORDER_OVERFLOW = -201
    OP_ERR_RQ_WRONG_INPUT = -202
    OP_ERR_ORD_WRONG_INPUT = -300
    OP_ERR_ORD_WRONG_ACCPWD = -301
    OP_ERR_ORD_WRONG_ACCNO = -302
    OP_ERR_ORD_WRONG_QTY200 = -303
    OP_ERR_ORD_WRONG_QTY400 = -304

    MSG_ERR_NONE = '정상처리'
    MSG_ERR_NO_LOGIN = '미접속상태'
    MSG_ERR_LOGIN = '로그인시 접속 실패 (아이피 오류 또는 접속정보 오류)'
    MSG_ERR_CONNECT = '서버 접속 실패'
    MSG_ERR_VERSION = '버전처리가 실패하였습니다.'
    MSG_ERR_TRCODE = 'TrCode 가 존재하지 않습니다.'
    MSG_ERR_NO_REGOPENAPI = '해외OpenAPI 미신청'
    MSG_ERR_SISE_OVERFLOW = '조회과부화'
    MSG_ERR_ORDER_OVERFLOW = '주문과부화'
    MSG_ERR_RQ_WRONG_INPUT = '조회입력값(명칭/누락) 오류'
    MSG_ERR_ORD_WRONG_INPUT = '주문입력갑 오류'
    MSG_ERR_ORD_WRONG_ACCPWD = '계좌비밀번호를 입력하십시오.'
    MSG_ERR_ORD_WRONG_ACCNO = '타인 계좌를 사용할 수 없습니다.'
    MSG_ERR_ORD_WRONG_QTY200 = '경고-주문수량 200개 초과'
    MSG_ERR_ORD_WRONG_QTY400 = '제한-주문수량 400개 초과'

    ERROR_MESSAGE_BY_CODE = {
        OP_ERR_NONE: MSG_ERR_NONE,
        OP_ERR_NO_LOGIN: MSG_ERR_NO_LOGIN,
        OP_ERR_LOGIN: MSG_ERR_LOGIN,
        OP_ERR_CONNECT: MSG_ERR_CONNECT,
        OP_ERR_VERSION: MSG_ERR_VERSION,
        OP_ERR_TRCODE: MSG_ERR_TRCODE,
        OP_ERR_NO_REGOPENAPI: MSG_ERR_NO_REGOPENAPI,
        OP_ERR_SISE_OVERFLOW: MSG_ERR_SISE_OVERFLOW,
        OP_ERR_ORDER_OVERFLOW: MSG_ERR_ORDER_OVERFLOW,
        OP_ERR_RQ_WRONG_INPUT: MSG_ERR_RQ_WRONG_INPUT,
        OP_ERR_ORD_WRONG_INPUT: MSG_ERR_ORD_WRONG_INPUT,
        OP_ERR_ORD_WRONG_ACCPWD: MSG_ERR_ORD_WRONG_ACCPWD,
        OP_ERR_ORD_WRONG_ACCNO: MSG_ERR_ORD_WRONG_ACCNO,
        OP_ERR_ORD_WRONG_QTY200: MSG_ERR_ORD_WRONG_QTY200,
        OP_ERR_ORD_WRONG_QTY400: MSG_ERR_ORD_WRONG_QTY400,
    }

    @classmethod
    def get_error_message_by_code(cls, code, default=None):
        return cls.ERROR_MESSAGE_BY_CODE.get(code, default)

    @classmethod
    def check_code_or_raise(cls, code):
        if code < 0:
            raise cls(code)
        return code

    @classmethod
    def wrap_to_check_code_or_raise(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cls.check_code_or_raise(func(*args, **kwargs))
        return wrapper

    @classmethod
    def try_or_raise(cls, arg, message=None):
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
        return '%s(%r, %r)' % (self.__class__.__name__, self._code, self._message)

    @property
    def code(self):
        return self._code

class KiwoomOpenApiWBooleanReturnCodeError(KiwoomOpenApiWError):

    OP_ERR_SUCCESS = 1
    OP_ERR_FAILURE = 0

    @classmethod
    def check_code_or_raise(cls, code, message=None):
        if not code:
            raise cls(message)
        return code

    @classmethod
    def wrap_to_check_code_or_raise(cls, func, message=None):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cls.check_code_or_raise(func(*args, **kwargs), message)
        return wrapper

    @classmethod
    def try_or_raise(cls, arg, message=None):
        if isinstance(arg, (int, bool)):
            return cls.check_code_or_raise(arg, message)
        elif callable(arg):
            return cls.wrap_to_check_code_or_raise(arg, message)
        else:
            raise TypeError("Expected 'int', 'bool' or 'callable' but %s found" % type(arg))

    def __init__(self, code, message=None):
        super().__init__(message)

        self._code = code
        self._message = message

    def __str__(self):
        if self._message:
            return self._message
        else:
            return self.__repr__()

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self._code, self._message)

    @property
    def code(self):
        return self._code
