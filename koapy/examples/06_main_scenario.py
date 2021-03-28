# 로깅 설정
import logging

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d',
    level=logging.DEBUG)

# KOAPY 임포트
from koapy import KiwoomOpenApiPlusEntrypoint

# 1. 엔트리포인트 객체 생성
entrypoint = KiwoomOpenApiPlusEntrypoint()

# 모듈 경로 확인 (기본 함수 사용 예시)
module_path = entrypoint.GetAPIModulePath()
print(module_path)

# 2. 로그인 예시
logging.info('Logging in...')
entrypoint.EnsureConnected()
logging.info('Logged in.')

# 3. 기본 함수 실행 예시

# 접속 상태 확인 (기본 함수 호출 예시)
logging.info('Checking connection status...')
status = entrypoint.GetConnectState()
logging.info('Connection status: %s', status)

# 종목 리스트 확인 (기본 함수 호출 예시)
logging.info('Getting stock codes and names...')
codes = entrypoint.GetCodeListByMarketAsList('0')
names = [entrypoint.GetMasterCodeName(code) for code in codes]

# 위에서 가져온 정보로 삼성전자의 code 확인
codes_by_name = dict(zip(names, codes))
logging.info('Checking stock code of Samsung...')
code = samsung_code = codes_by_name['삼성전자']
logging.info('Code of Samsung: %s', code)

# 4. TR 요청 예시

# 상위 함수를 활용한 TR 요청 예시 (opt10001)
logging.info('Getting basic info of Samsung...')
info = entrypoint.GetStockBasicInfoAsDict(code)
logging.info('Got basic info data (using GetStockBasicInfoAsDict):')
print(info)

# 상위 함수를 활용한 TR 요청 예시 (opt10081)
logging.info('Getting daily stock data of Samsung...')
data = entrypoint.GetDailyStockDataAsDataFrame(code)
logging.info('Got daily stock data:')
print(data)

# 하위 함수를 사용한 TR 요청 예시 (opt10001)
rqname = '주식기본정보요청'
trcode = 'opt10001'
screen_no = '0001' # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정
inputs = {'종목코드': code}

output = {}

logging.info('Requesting data for request name: %s', rqname)
for event in entrypoint.TransactionCall(rqname, trcode, screen_no, inputs):
    logging.info('Got event for request: %s', rqname)
    names = event.single_data.names
    values = event.single_data.values
    for name, value in zip(names, values):
        output[name] = value

logging.info('Got basic info data (using TransactionCall):')
print(output)

# (디버깅을 위한) 이벤트 메시지 출력 함수
from pprint import PrettyPrinter
from google.protobuf.json_format import MessageToDict

pp = PrettyPrinter()

def pprint_event(event):
    pp.pprint(MessageToDict(event, preserving_proto_field_name=True))

logging.info('Last event message was:')
pprint_event(event)

# TR 관련 메타정보 확인
from koapy import KiwoomOpenApiPlusTrInfo

logging.info('Checking TR info of opt10001')
tr_info = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code('opt10001')

logging.info('Inputs of opt10001:')
print(tr_info.inputs)
logging.info('Single outputs of opt10001:')
print(tr_info.single_outputs)
logging.info('Multi outputs of opt10001:')
print(tr_info.multi_outputs)

# 5. 조건검색 예시

# 조건검색 설정 불러오기
entrypoint.EnsureConditionLoaded()

# 일반 조건검색 예시
condition_name = '대형 저평가 우량주'

logging.info('Getting stock codes with condition: %s', condition_name)
codes, info = entrypoint.GetCodeListByCondition(condition_name, with_info=True)

print(codes)
print(info)

# 실시간 조건검색 예시
condition_name = '중소형 저평가주'

logging.info('Start listening realtime condition stream...')
stream = entrypoint.GetCodeListByConditionAsStream(condition_name)

# 이벤트 스트림을 도중에 멈추기 위해서 threading.Timer 활용
import threading

def stop_listening_cond():
    logging.info('Stop listening realtime events...')
    stream.cancel()

threading.Timer(10.0, stop_listening_cond).start() # 10초 이후에 gRPC 커넥션 종료하도록 설정

# 이벤트 불러와서 출력처리
import grpc

try:
    for i, (inserted, deleted) in enumerate(stream):
        print('index: %d, inserted: %s, deleted: %s' % (i, inserted, deleted))
except grpc.RpcError as e:
    pass

# 6.주문처리 예시

# 현재 시장이 열려 있는지 (주문이 가능한지) 확인하는 함수
from pandas import Timestamp
from exchange_calendars import get_calendar

krx_calendar = get_calendar('XKRX')

def is_currently_in_session():
    now = Timestamp.now(tz=krx_calendar.tz)
    previous_open = krx_calendar.previous_open(now).astimezone(krx_calendar.tz)
    next_close = krx_calendar.next_close(previous_open).astimezone(krx_calendar.tz)
    return previous_open <= now <= next_close

# 주문처리 파라미터 설정
first_account_no = entrypoint.GetFirstAvailableAccount()

request_name = '삼성전자 1주 시장가 신규 매수' # 사용자 구분명, 구분가능한 임의의 문자열
screen_no = '0001'                           # 화면번호, 0000 을 제외한 4자리 숫자 임의로 지정
account_no = first_account_no                # 계좌번호 10자리, 여기서는 계좌번호 목록에서 첫번째로 발견한 계좌번호로 매수처리
order_type = 1         # 주문유형, 1 : 신규매수
code = samsung_code    # 종목코드, 앞의 삼성전자 종목코드
quantity = 1           # 주문수량, 1주 매수
price = 0              # 주문가격, 시장가 매수는 가격설정 의미없음
quote_type = '03'      # 거래구분, 03 : 시장가
original_order_no = '' # 원주문번호, 주문 정정/취소 등에서 사용

# 현재는 기본적으로 주문수량이 모두 소진되기 전까지 이벤트를 듣도록 되어있음 (단순 호출 예시)
if is_currently_in_session():
    logging.info('Sending order to buy %s, quantity of 1 stock, at market price...', code)
    for event in entrypoint.OrderCall(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no):
        pprint_event(event)
else:
    logging.info('Cannot send an order while market is not open, skipping...')

# 7. 실시간 데이터 처리 예시
from koapy import KiwoomOpenApiPlusRealType

code_list = [code]
fid_list = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name('주식시세')
real_type = '0' # 기존 화면에 추가가 아니라 신규 생성

# 현재는 기본적으로 실시간 이벤트를 무한정 가져옴 (커넥션 컨트롤 가능한 예시)
logging.info('Starting to get realtime stock data for code: %s', code)
stream = entrypoint.GetRealDataForCodesAsStream(code_list, fid_list, real_type, screen_no=None, infer_fids=True, readable_names=True, fast_parse=False)

# 이벤트 스트림을 도중에 멈추기 위해서 threading.Timer 활용
import threading

def stop_listening_real():
    logging.info('Stop listening realtime events...')
    stream.cancel()

threading.Timer(10.0, stop_listening_real).start() # 10초 이후에 gRPC 커넥션 종료하도록 설정

# 이벤트 불러와서 출력처리
import grpc

try:
    for event in stream:
        pprint_event(event)
except grpc.RpcError as e:
    print(e)

# 예시 스크립트 끝
logging.info('End of example')

# 리소스 해제
entrypoint.close()
