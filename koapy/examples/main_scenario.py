import threading

from koapy import KiwoomOpenApiContext
from koapy import RealType

from pprint import PrettyPrinter
from google.protobuf.json_format import MessageToDict

pp = PrettyPrinter()

with KiwoomOpenApiContext() as context:
    # 로그인 예시
    print('Logging in...')
    context.EnsureConnected()
    print('Logged in.')

    # 기본 함수 호출 예시
    print('Getting stock codes and names...')
    codes = context.GetCodeListByMarketAsList('0')
    names = [context.GetMasterCodeName(code) for code in codes]

    # 위에서 가져온 정보로 삼성전자의 code 확인
    codes_by_name = dict(zip(names, codes))
    print('Checking stock code of Samsung...')
    samsung_code = codes_by_name['삼성전자']
    code = samsung_code
    print('Code: %s' % code)

    # TR 예시 (opt10081)
    print('Getting daily stock data of Samsung...')
    data = context.GetDailyStockDataAsDataFrame(code)
    print('Daily stock data:')
    print(data)

    # 조건검색 예시
    condition_name = '대형 저평가 우량주'
    print('Getting stock codes with condition: %s' % condition_name)
    codes, info = context.GetCodeListByCondition(condition_name, with_info=True)
    print(codes)
    print(info)

    # 주문처리 예시
    first_account_no = context.GetFirstAvailableAccount()

    request_name = '삼성전자 1주 시장가 신규 매수' # 사용자 구분명, 구분가능한 임의의 문자열
    screen_no = '0001'                           # 화면번호
    account_no = first_account_no                # 계좌번호 10자리, 여기서는 계좌번호 목록에서 첫번째로 발견한 계좌번호로 매수처리
    order_type = 1         # 주문유형, 1 : 신규매수
    code = samsung_code    # 종목코드, 앞의 삼성전자 종목코드
    quantity = 1           # 주문수량, 1주 매수
    price = 0              # 주문가격, 시장가 매수는 가격설정 의미없음
    quote_type = '03'      # 거래구분, 03 : 시장가
    original_order_no = '' # 원주문번호, 주문 정정/취소 등에서 사용

    # 현재는 기본적으로 주문수량이 모두 소진되기 전까지 이벤트를 듣도록 되어있음 (단순 호출 예시)
    print('Sending order to buy %s, quantity of 1 stock, at market price...' % code)
    for event in context.OrderCall(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no):
        pp.pprint(MessageToDict(event))

    # 실시간 예시
    code_list = [code]
    fid_list = RealType.get_fids_by_realtype('주식시세')
    real_type = '0'

    # 현재는 기본적으로 실시간 이벤트를 무한정 가져옴 (커넥션 컨트롤 가능한 예시)
    print('Starting to get realtime stock data for code: %s' % code)
    events = context.GetRealDataForCodesAsStream(code_list, fid_list, real_type, screen_no=None, infer_fids=True, readable_names=True, fast_parse=False)

    def stop_listening():
        print('Stopping to listen events...')
        events.cancel()

    threading.Timer(10.0, stop_listening).start() # 10초 이후에 gRPC 커넥션 종료하도록 설정

    # 이벤트 불러와서 출력처리
    for event in events:
        pp.pprint(MessageToDict(event))
