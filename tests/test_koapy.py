import itertools
import re

import pandas as pd
import pytest

from pandas.testing import assert_series_equal

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLib import (
    API_MODULE_PATH,
)
from koapy.utils.exchange_calendars import is_currently_in_session
from koapy.utils.platform import is_32bit, is_windows

# pylint: disable=redefined-outer-name


def is_ocx_available():
    if is_windows() and is_32bit():
        return API_MODULE_PATH and API_MODULE_PATH.exists()
    return False


skipif_ocx_not_available = pytest.mark.skipif(
    not is_ocx_available(),
    reason="Features using OCX can be tested only in windows 32bit and OpenAPI installed",
)

skipif_not_currently_in_session = pytest.mark.skipif(
    not is_currently_in_session(),
    reason="Cannot test this feature while market is not open",
)


@pytest.fixture(scope="module")
def entrypoint():
    from koapy import KiwoomOpenApiPlusEntrypoint

    with KiwoomOpenApiPlusEntrypoint() as entrypoint:
        entrypoint.EnsureConnected()
        assert entrypoint.IsSimulationServer()
        yield entrypoint


@pytest.fixture(scope="module")
def calendar():
    from exchange_calendars import get_calendar

    calendar = get_calendar("XKRX")
    return calendar


@pytest.fixture(scope="module")
def downloader():
    from koapy.utils.data import KrxHistoricalDailyPriceDataDownloader

    downloader = KrxHistoricalDailyPriceDataDownloader()
    return downloader


@skipif_ocx_not_available
def test_GetConnectState(entrypoint):
    assert (
        entrypoint.GetConnectState() == 1
    ), "Entrypoint fixture should be in connected state"


@skipif_ocx_not_available
def test_GetCodeListByMarket(entrypoint):
    code = "005930"
    codes = entrypoint.GetCodeListByMarketAsList("0")
    assert (
        code in codes
    ), "Samsung Electronics not in market, which is unlikely to happen"


@skipif_ocx_not_available
def test_GetMasterCodeName(entrypoint):
    code = "005930"
    name = entrypoint.GetMasterCodeName(code)
    assert (
        name == "삼성전자"
    ), "Failed to get Samsung Electronics from code, which is unlikely to happen"


@skipif_ocx_not_available
def test_KiwoomOpenApiPlusTrInfo():
    from koapy import KiwoomOpenApiPlusTrInfo

    tr_code = "opt10001"
    tr_info = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code(tr_code)
    tr_info_from_dump = KiwoomOpenApiPlusTrInfo.trinfo_by_code_from_dump_file()
    tr_info_from_dump = tr_info_from_dump.get(tr_code)

    assert tr_info == tr_info_from_dump


@skipif_ocx_not_available
def test_GetStockBasicInfoAsDict(entrypoint):
    code = "005930"
    info = entrypoint.GetStockBasicInfoAsDict(code)
    name = info["종목명"]
    assert (
        name == "삼성전자"
    ), "Failed to get Samsung Electronics from code, which is unlikely to happen"


@skipif_ocx_not_available
def test_GetDailyStockDataAsDataFrame(entrypoint, calendar, downloader):
    code = "005930"

    now = pd.Timestamp.now(calendar.tz).floor("T")
    start_date = calendar.previous_close(now).astimezone(calendar.tz).normalize()
    end_date = start_date - 5 * calendar.day

    data = entrypoint.GetDailyStockDataAsDataFrame(
        code, start_date=start_date, end_date=end_date
    )
    data_krx = downloader.download(code, end_date + calendar.day, start_date)

    data_dates = pd.to_datetime(data["일자"], format="%Y%m%d")
    data_krx_dates = data_krx.index.to_series()
    assert_series_equal(
        data_dates, data_krx_dates, check_names=False, check_index=False
    )

    data_closes = pd.to_numeric(data["현재가"])
    data_krx_closes = data_krx["Close"]
    assert_series_equal(
        data_closes, data_krx_closes, check_names=False, check_index=False
    )


@skipif_ocx_not_available
@skipif_not_currently_in_session
def test_GetCodeListByCondition(entrypoint):
    entrypoint.EnsureConditionLoaded()

    conditions = entrypoint.GetConditionNameListAsList()
    condition_name = "대형 저평가 우량주"
    assert condition_name in [item[1] for item in conditions]

    codes, info = entrypoint.GetCodeListByCondition(condition_name, with_info=True)
    assert len(codes) > 0
    assert info.shape[0] > 0

    info_codes = info["종목코드"].tolist()
    for code in codes:
        assert code in info_codes


@skipif_ocx_not_available
@skipif_not_currently_in_session
def test_GetCodeListByConditionAsStream(entrypoint):
    entrypoint.EnsureConditionLoaded()

    conditions = entrypoint.GetConditionNameListAsList()
    condition_name = "중소형 저평가주"
    assert condition_name in [item[1] for item in conditions]

    stream = entrypoint.GetCodeListByConditionAsStream(condition_name, with_info=True)

    condition_event = next(stream)
    info_event = next(stream)

    stream.cancel()

    codes = condition_event.arguments[1].string_value.strip(";").split(";")
    records = [values.values for values in info_event.multi_data.values]
    columns = info_event.multi_data.names

    info = pd.DataFrame.from_records(records, columns=columns)
    assert len(codes) > 0
    assert info.shape[0] > 0

    info_codes = info["종목코드"].tolist()
    for code in codes:
        assert code in info_codes


@skipif_ocx_not_available
@skipif_not_currently_in_session
def test_OrderCall(entrypoint):
    first_account_no = entrypoint.GetFirstAvailableAccount()
    request_name = "삼성전자 1주 시장가 신규 매수"  # 사용자 구분명, 구분가능한 임의의 문자열
    screen_no = "0001"  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
    account_no = first_account_no  # 계좌번호 10자리, 여기서는 계좌번호 목록에서 첫번째로 발견한 계좌번호로 매수처리
    order_type = 1  # 주문유형, 1 : 신규매수
    code = "005930"  # 종목코드, 앞의 삼성전자 종목코드
    quantity = 1  # 주문수량, 1주 매수
    price = 0  # 주문가격, 시장가 매수는 가격설정 의미없음
    quote_type = "03"  # 거래구분, 03 : 시장가
    original_order_no = ""  # 원주문번호, 주문 정정/취소 등에서 사용

    stream = entrypoint.OrderCall(
        request_name,
        screen_no,
        account_no,
        order_type,
        code,
        quantity,
        price,
        quote_type,
        original_order_no,
    )

    on_receive_msg = next(stream)  # 주문완료
    on_receive_tr_data = next(stream)  # 주문성공
    on_receive_chejan_data1 = next(stream)  # 주문접수
    on_receive_chejan_data2 = next(stream)  # 주문체결
    on_receive_chejan_data3 = next(stream)  # 주문잔고

    assert on_receive_msg.name == "OnReceiveMsg"
    assert on_receive_msg.arguments[0].string_value == screen_no
    assert on_receive_msg.arguments[1].string_value == request_name

    assert on_receive_tr_data.name == "OnReceiveTrData"
    assert on_receive_tr_data.single_data.names[0] == "주문번호"
    order_no = on_receive_tr_data.single_data.values[0]
    assert re.match(r"^\d+$", order_no)

    assert on_receive_chejan_data1.name == "OnReceiveChejanData"
    data = dict(
        zip(
            on_receive_chejan_data1.single_data.names,
            on_receive_chejan_data1.single_data.values,
        )
    )
    assert data["계좌번호"] == account_no
    assert data["주문번호"] == order_no
    assert data["종목코드"] == f"A{code}"
    assert data["주문상태"] == "접수"
    assert data["종목명"] == entrypoint.GetMasterCodeName(code)
    assert int(data["주문수량"]) == quantity
    assert int(data["주문가격"]) == price
    assert int(data["미체결수량"]) == quantity
    assert int(data["체결누계금액"]) == 0
    assert data["주문구분"] == "+매수"
    assert data["매매구분"] == "시장가"
    assert data["화면번호"] == screen_no

    assert on_receive_chejan_data2.name == "OnReceiveChejanData"
    data = dict(
        zip(
            on_receive_chejan_data2.single_data.names,
            on_receive_chejan_data2.single_data.values,
        )
    )
    assert data["계좌번호"] == account_no
    assert data["주문번호"] == order_no
    assert data["종목코드"] == f"A{code}"
    assert data["주문상태"] == "체결"
    assert data["종목명"] == entrypoint.GetMasterCodeName(code)
    assert int(data["주문수량"]) == quantity
    assert int(data["주문가격"]) == price
    assert int(data["미체결수량"]) < quantity
    assert int(data["체결누계금액"]) > 0
    assert data["주문구분"] == "+매수"
    assert data["매매구분"] == "시장가"
    assert data["화면번호"] == screen_no
    assert re.match(r"^\d+$", data["체결번호"])
    assert re.match(r"^\d+$", data["체결가"])
    assert re.match(r"^\d+$", data["체결량"])

    assert on_receive_chejan_data3.name == "OnReceiveChejanData"
    data = dict(
        zip(
            on_receive_chejan_data3.single_data.names,
            on_receive_chejan_data3.single_data.values,
        )
    )
    assert data["계좌번호"] == account_no
    assert data["종목코드"] == f"A{code}"
    assert data["종목명"] == entrypoint.GetMasterCodeName(code)
    assert int(data["보유수량"]) > 0
    assert int(data["매입단가"]) > 0
    assert int(data["총매입가"]) > 0


@skipif_ocx_not_available
def test_KiwoomOpenApiPlusRealType():
    from koapy import KiwoomOpenApiPlusRealType

    realtype_name = "주식시세"
    realtype_info = KiwoomOpenApiPlusRealType.get_realtype_info_by_realtype_name(
        realtype_name
    )
    realtype_info_from_dump = (
        KiwoomOpenApiPlusRealType.realtype_by_desc_from_dump_file()
    )
    realtype_info_from_dump = realtype_info_from_dump.get(realtype_name)

    assert realtype_info == realtype_info_from_dump


@skipif_ocx_not_available
@skipif_not_currently_in_session
def test_GetRealDataForCodesAsStream(entrypoint):
    from koapy import KiwoomOpenApiPlusRealType

    code = "005930"
    realtype_name = "주식시세"

    code_list = [code]
    fid_list = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name(realtype_name)
    opt_type = "0"  # 기존 화면에 추가가 아니라 신규 생성, 1 의 경우 기존 화면번호에 추가

    stream = entrypoint.GetRealDataForCodesAsStream(
        code_list,
        fid_list,
        opt_type,
        screen_no=None,  # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정, None 의 경우 내부적으로 화면번호 자동할당
        infer_fids=True,  # True 로 설정 시 주어진 fid_list 를 고집하지 말고 이벤트 처리 함수의 인자로 전달받는 실시간데이터 이름에 따라 유연하게 fid_list 를 추론
        readable_names=True,  # True 로 설정 시 각 fid 마다 숫자 대신 읽을 수 있는 이름으로 변환하여 반환
        fast_parse=False,  # True 로 설정 시 이벤트 처리 함수내에서 데이터 값 읽기 시 GetCommRealData() 함수 호출 대신, 이벤트 처리 함수의 인자로 넘어오는 데이터를 직접 활용, infer_fids 가 True 로 설정된 경우만 유의미함
    )
    check_count = 10
    events = itertools.islice(stream, check_count)
    events = list(events)
    stream.cancel()

    for event in events:
        assert event.name == "OnReceiveRealData"
        assert event.arguments[0].string_value == code
        assert event.arguments[1].string_value in ["주식체결"]
