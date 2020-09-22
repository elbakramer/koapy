from koapy.context.KiwoomOpenApiContext import KiwoomOpenApiContext
from koapy.openapi.RealType import RealType

from google.protobuf.json_format import MessageToDict

with KiwoomOpenApiContext() as context:
    # 로그인 예시
    context.EnsureConnected()

    # 함수 호출 예시
    codes = context.GetCodeListByMarketAsList('0')
    names = [context.GetMasterCodeName(code) for code in codes]

    codes_by_name = dict(zip(names, codes))
    code = codes_by_name['삼성전자']

    # TR 예시 (opt10081)
    data = context.GetDailyStockDataAsDataFrame(code)
    print(data)

    # 실시간 예시
    screen_no = '0001'
    code_list = [code]
    fid_list = RealType.get_fids_by_realtype('주식시세')
    real_type = '0'

    for event in context.RealCall(screen_no, code_list, fid_list, real_type):
        print(MessageToDict(event))
