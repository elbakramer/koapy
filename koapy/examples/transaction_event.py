from koapy import KiwoomOpenApiContext

with KiwoomOpenApiContext() as context:
    context.EnsureConnected()

    code = '005930'
    price = context.GetStockInfoAsDataFrame(code).loc[0, '현재가']
    print(price)

    # or... what happens inside...

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
    price = output['현재가']
    print(price)
