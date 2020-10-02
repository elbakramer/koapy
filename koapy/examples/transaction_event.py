from koapy import KiwoomOpenApiContext

with KiwoomOpenApiContext() as context:
    context.EnsureConnected()

    # 이벤트를 알아서 처리하고 결과물만 제공하는 상위 함수 사용 예시
    code = '005930'
    info = context.GetStockInfoAsDataFrame(code)
    print(info)
    price = info.loc[0, '현재가']
    print(price)

    # 이벤트를 스트림으로 반환하는 하위 함수 직접 사용 예시 (위의 상위 함수 내부에서 실제로 처리되는 내용에 해당)
    rqname = 'get_stock_info'
    trcode = 'opt10001'
    screenno = '0001'
    inputs = {'종목코드': code}
    output = {}

    for event in context.TransactionCall(rqname, trcode, screenno, inputs):
        names = event.listen_response.single_data.names
        values = event.listen_response.single_data.values
        for name, value in zip(names, values):
            output[name] = value

    print(output)

    price = output['현재가']
    print(price)
