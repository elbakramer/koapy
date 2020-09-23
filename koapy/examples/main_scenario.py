from koapy import KiwoomOpenApiContext
from koapy import RealType

from pprint import PrettyPrinter
from google.protobuf.json_format import MessageToDict

with KiwoomOpenApiContext() as context:
    # 로그인 예시
    print('Logging in...')
    context.EnsureConnected()
    print('Logged in.')

    # 함수 호출 예시
    print('Getting stock codes and names...')
    codes = context.GetCodeListByMarketAsList('0')
    names = [context.GetMasterCodeName(code) for code in codes]

    codes_by_name = dict(zip(names, codes))
    print('Checking stock code of Samsung...')
    code = codes_by_name['삼성전자']
    print('Code: %s' % code)

    # TR 예시 (opt10081)
    print('Getting daily stock data of Samsung...')
    data = context.GetDailyStockDataAsDataFrame(code)
    print('Daily stock data:')
    print(data)

    # 실시간 예시
    code_list = [code]
    fid_list = RealType.get_fids_by_realtype('주식시세')
    real_type = '0'

    pp = PrettyPrinter()

    print('Starting to get realtime stock data for code: %s' % code)
    for event in context.WatchRealDataForCodesAsStream(code_list, fid_list, real_type, screen_no=None, infer_fids=True, readable_names=True, fast_parse=False):
        pp.pprint(MessageToDict(event))
