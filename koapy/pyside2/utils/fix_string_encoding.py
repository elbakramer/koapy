import chardet
import logging

from functools import wraps

def run_until_returns_true(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if wrapper.should_run:
            result = f(*args, **kwargs)
            if result:
                wrapper.should_run = False
            return result
    wrapper.should_run = True
    return wrapper

@run_until_returns_true
def test_and_warn_once(byte_string, enc, dec):
    detected = chardet.detect(byte_string)
    detected_encoding = detected['encoding']
    result = detected_encoding != enc and detected_encoding == dec
    if result:
        logging.warning('Fixed string encoding from %s to %s', byte_string.decode(enc), byte_string.decode(dec))
    return result

def fix_string_encoding(arg, enc=None, dec=None):
    """
    아래와 같은 방법들로 서버를 열고 접근해 값을 가져오는 경우 인코딩이 꼬이는 이슈가 있음.
    - 최초 conda run 형태로 koapy serve 실행 (여기서부터 뭔가 꼬이는 듯)
    - 이후 같은 쉘에서 아무 다른 방식으로 실행
    근본적인 원인 및 해결법도 아직 모르겠고 이게 다른 환경에서도 재발 가능한지도 잘 모르는 상황.
    대신 아래를 모든 함수 결과 및 이벤트 콜백 함수 인자에 적용하면 어찌어찌 복원은 가능한 것 확인.
    """

    if not isinstance(arg, str):
        return arg

    possibly_decoded_wrong = arg

    if enc is None:
        enc = 'ascii'
    if dec is None:
        dec = 'cp949'

    try:
        byte_string = possibly_decoded_wrong.encode(enc)
    except UnicodeEncodeError:
        return arg

    try:
        restored_string = byte_string.decode(dec)
    except UnicodeDecodeError:
        return arg

    test_and_warn_once(byte_string, enc, dec)

    return restored_string
