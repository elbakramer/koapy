from koapy import KiwoomOpenApiContext

with KiwoomOpenApiContext() as context:
    # 로그인 처리
    context.EnsureConnected()

    # 이벤트를 알아서 처리하고 결과물만 제공하는 상위 함수 사용 예시
    code = '005930'
    info = context.GetStockInfoAsDataFrame(code)
    print(info)
    price = info.loc[0, '현재가']
    print(price)

    # 이벤트를 스트림으로 반환하는 하위 함수 직접 사용 예시 (위의 상위 함수 내부에서 실제로 처리되는 내용에 해당)
    rqname = '주식기본정보요청'
    trcode = 'opt10001'
    screenno = '0001'
    inputs = {'종목코드': code}
    output = {}

    # 아래의 함수는 gRPC 서비스의 rpc 함수를 호출함, 따라서 event 메시지의 구조는 KiwoomOpenApiService.proto 파일 참조
    for event in context.TransactionCall(rqname, trcode, screenno, inputs):
        names = event.listen_response.single_data.names
        values = event.listen_response.single_data.values
        for name, value in zip(names, values):
            output[name] = value

    # 전체 결과 출력 (싱글데이터)
    print(output)

    # 현재가 값만 출력
    price = output['현재가']
    print(price)
