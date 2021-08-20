from concurrent.futures import Future
from functools import wraps


class KiwoomOpenApiPlusError(Exception):
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
        return KiwoomOpenApiPlusNegativeReturnCodeError.try_or_raise(arg, message)

    @classmethod
    def try_or_raise_boolean(cls, arg, message):
        return KiwoomOpenApiPlusBooleanReturnCodeError.try_or_raise(arg, message)

    @classmethod
    def get_error_message_by_code(cls, code, default=None):
        return KiwoomOpenApiPlusNegativeReturnCodeError.get_error_message_by_code(
            code, default
        )


class KiwoomOpenApiPlusNegativeReturnCodeError(KiwoomOpenApiPlusError):

    OP_ERR_NONE = 0
    OP_ERR_FAIL = -10
    OP_ERR_COND_NOTFOUND = -11
    OP_ERR_COND_MISMATCH = -12
    OP_ERR_COND_OVERFLOW = -13
    OP_ERR_TR_FAIL = -22
    OP_ERR_LOGIN = -100
    OP_ERR_CONNECT = -101
    OP_ERR_VERSION = -102
    OP_ERR_FIREWALL = -103
    OP_ERR_MEMORY = -104
    OP_ERR_INPUT = -105
    OP_ERR_SOCKET_CLOSED = -106
    OP_ERR_SISE_OVERFLOW = -200
    OP_ERR_RQ_STRUCT_FAIL = -201
    OP_ERR_RQ_STRING_FAIL = -202
    OP_ERR_NO_DATA = -203
    OP_ERR_OVER_MAX_DATA = -204
    OP_ERR_DATA_RCV_FAIL = -205
    OP_ERR_OVER_MAX_FID = -206
    OP_ERR_REAL_CANCEL = -207
    OP_ERR_ORD_WRONG_INPUT = -300
    OP_ERR_ORD_WRONG_ACCTNO = -301
    OP_ERR_OTHER_ACC_USE = -302
    OP_ERR_MIS_2BILL_EXC = -303
    OP_ERR_MIS_5BILL_EXC = -304
    OP_ERR_MIS_1PER_EXC = -305
    OP_ERR_MIS_3PER_EXC = -306
    OP_ERR_SEND_FAIL = -307
    OP_ERR_ORD_OVERFLOW = -308
    OP_ERR_ORD_OVERFLOW2 = -311
    OP_ERR_MIS_300CNT_EXC = -309
    OP_ERR_MIS_500CNT_EXC = -310
    OP_ERR_ORD_WRONG_ACCTINFO = -340
    OP_ERR_ORD_SYMCODE_EMPTY = -500

    MSG_ERR_NONE = "정상처리"
    MSG_ERR_FAIL = "실패"
    MSG_ERR_COND_NOTFOUND = "조건번호 없음"
    MSG_ERR_COND_MISMATCH = "조건번호와 조건식 틀림"
    MSG_ERR_COND_OVERFLOW = "조건검색 조회요청 초과"
    MSG_ERR_TR_FAIL = "전문 처리 실패"
    MSG_ERR_LOGIN = "사용자정보 교환 실패"
    MSG_ERR_CONNECT = "서버접속 실패"
    MSG_ERR_VERSION = "버전처리 실패"
    MSG_ERR_FIREWALL = "개인방화벽 실패"
    MSG_ERR_MEMORY = "메모리보호 실패"
    MSG_ERR_INPUT = "함수입력값 오류"
    MSG_ERR_SOCKET_CLOSED = "통신 연결종료"
    MSG_ERR_SISE_OVERFLOW = "시세조회 과부하"
    MSG_ERR_RQ_STRUCT_FAIL = "전문작성 초기화 실패"
    MSG_ERR_RQ_STRING_FAIL = "전문작성 입력값 오류"
    MSG_ERR_NO_DATA = "데이터 없음"
    MSG_ERR_OVER_MAX_DATA = "조회 가능한 종목수 초과"
    MSG_ERR_DATA_RCV_FAIL = "데이터수신 실패"
    MSG_ERR_OVER_MAX_FID = "조회 가능한 FID수 초과"
    MSG_ERR_REAL_CANCEL = "실시간 해제 오류"
    MSG_ERR_ORD_WRONG_INPUT = "입력값 오류"
    MSG_ERR_ORD_WRONG_ACCTNO = "계좌 비밀번호 없음"
    MSG_ERR_OTHER_ACC_USE = "타인계좌사용 오류"
    MSG_ERR_MIS_2BILL_EXC = "주문가격이 20억원을 초과"
    MSG_ERR_MIS_5BILL_EXC = "주문가격이 50억원을 초과"
    MSG_ERR_MIS_1PER_EXC = "주문수량이 총발행주수의 1%초과오류"
    MSG_ERR_MIS_3PER_EXC = "주문수량이 총발행주수의 3%초과오류"
    MSG_ERR_SEND_FAIL = "주문전송 실패"
    MSG_ERR_ORD_OVERFLOW = "주문전송 과부하"
    MSG_ERR_ORD_OVERFLOW2 = "주문전송 과부하"
    MSG_ERR_MIS_300CNT_EXC = "주문수량 300계약 초과"
    MSG_ERR_MIS_500CNT_EXC = "주문수량 500계약 초과"
    MSG_ERR_ORD_WRONG_ACCTINFO = "계좌정보없음"
    MSG_ERR_ORD_SYMCODE_EMPTY = "종목코드없음"

    ERROR_MESSAGE_BY_CODE = {
        OP_ERR_NONE: MSG_ERR_NONE,
        OP_ERR_FAIL: MSG_ERR_FAIL,
        OP_ERR_COND_NOTFOUND: MSG_ERR_COND_NOTFOUND,
        OP_ERR_COND_MISMATCH: MSG_ERR_COND_MISMATCH,
        OP_ERR_COND_OVERFLOW: MSG_ERR_COND_OVERFLOW,
        OP_ERR_TR_FAIL: MSG_ERR_TR_FAIL,
        OP_ERR_LOGIN: MSG_ERR_LOGIN,
        OP_ERR_CONNECT: MSG_ERR_CONNECT,
        OP_ERR_VERSION: MSG_ERR_VERSION,
        OP_ERR_FIREWALL: MSG_ERR_FIREWALL,
        OP_ERR_MEMORY: MSG_ERR_MEMORY,
        OP_ERR_INPUT: MSG_ERR_INPUT,
        OP_ERR_SOCKET_CLOSED: MSG_ERR_SOCKET_CLOSED,
        OP_ERR_SISE_OVERFLOW: MSG_ERR_SISE_OVERFLOW,
        OP_ERR_RQ_STRUCT_FAIL: MSG_ERR_RQ_STRUCT_FAIL,
        OP_ERR_RQ_STRING_FAIL: MSG_ERR_RQ_STRING_FAIL,
        OP_ERR_NO_DATA: MSG_ERR_NO_DATA,
        OP_ERR_OVER_MAX_DATA: MSG_ERR_OVER_MAX_DATA,
        OP_ERR_DATA_RCV_FAIL: MSG_ERR_DATA_RCV_FAIL,
        OP_ERR_OVER_MAX_FID: MSG_ERR_OVER_MAX_FID,
        OP_ERR_REAL_CANCEL: MSG_ERR_REAL_CANCEL,
        OP_ERR_ORD_WRONG_INPUT: MSG_ERR_ORD_WRONG_INPUT,
        OP_ERR_ORD_WRONG_ACCTNO: MSG_ERR_ORD_WRONG_ACCTNO,
        OP_ERR_OTHER_ACC_USE: MSG_ERR_OTHER_ACC_USE,
        OP_ERR_MIS_2BILL_EXC: MSG_ERR_MIS_2BILL_EXC,
        OP_ERR_MIS_5BILL_EXC: MSG_ERR_MIS_5BILL_EXC,
        OP_ERR_MIS_1PER_EXC: MSG_ERR_MIS_1PER_EXC,
        OP_ERR_MIS_3PER_EXC: MSG_ERR_MIS_3PER_EXC,
        OP_ERR_SEND_FAIL: MSG_ERR_SEND_FAIL,
        OP_ERR_ORD_OVERFLOW: MSG_ERR_ORD_OVERFLOW,
        OP_ERR_ORD_OVERFLOW2: MSG_ERR_ORD_OVERFLOW2,
        OP_ERR_MIS_300CNT_EXC: MSG_ERR_MIS_300CNT_EXC,
        OP_ERR_MIS_500CNT_EXC: MSG_ERR_MIS_500CNT_EXC,
        OP_ERR_ORD_WRONG_ACCTINFO: MSG_ERR_ORD_WRONG_ACCTINFO,
        OP_ERR_ORD_SYMCODE_EMPTY: MSG_ERR_ORD_SYMCODE_EMPTY,
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
        if isinstance(arg, Future):

            def callback(future):
                exc = future.exception()
                if exc:
                    raise exc
                result = future.result()
                cls.try_or_raise(result, message)

            arg.add_done_callback(callback)
            return arg
        elif isinstance(arg, int):
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
        return "{}({!r}, {!r})".format(
            self.__class__.__name__, self._code, self._message
        )

    @property
    def code(self):
        return self._code


class KiwoomOpenApiPlusBooleanReturnCodeError(KiwoomOpenApiPlusError):

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
        if isinstance(arg, Future):

            def callback(future):
                exc = future.exception()
                if exc:
                    raise exc
                result = future.result()
                cls.try_or_raise(result, message)

            arg.add_done_callback(callback)
            return arg
        elif isinstance(arg, (int, bool)):
            return cls.check_code_or_raise(arg, message)
        elif callable(arg):
            return cls.wrap_to_check_code_or_raise(arg, message)
        else:
            raise TypeError(
                "Expected 'int', 'bool' or 'callable' but %s found" % type(arg)
            )

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
        return "{}({!r}, {!r})".format(
            self.__class__.__name__, self._code, self._message
        )

    @property
    def code(self):
        return self._code
