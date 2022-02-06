:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper`
===========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper.KiwoomOpenApiPlusServiceClientStubCoreWrapper
   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper.KiwoomOpenApiPlusServiceClientStubExtendedWrapper
   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper.KiwoomOpenApiPlusServiceClientStubWrapper




.. py:class:: KiwoomOpenApiPlusServiceClientStubCoreWrapper(stub, executor)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusQAxWidgetUniversalMixin`

   KiwoomOpenApiPlusServiceServicer 에서 구현되어 이후 Stub 을 통해 제공되는
   RPC 들을 클라이언트에서 좀 더 쉽게 사용하기 위한 래퍼 함수들을 제공합니다.

   .. py:attribute:: METHOD_NAMES
      

      

   .. py:attribute:: EVENT_NAMES
      

      

   .. py:method:: Call(self, name, *args)

      임의의 함수 호출을 위한 RPC 입니다.

      함수의 이름과 파라미터를 요청 메시지를 통해 전달받아 서버측에서 해당 함수를 호출하고
      호출결과를 응답 메시지를 통해 전달합니다.

      함수의 파라미터와 리턴값은 문자열/숫자/불리언 등의 단순한 타입만 지원합니다.


   .. py:method:: LoginCall(self, credentials=None)

      키움증권 서버 연결 시나리오에 해당하는 RPC 입니다.

      CommConnect() 메소드 호출 이후 발생하는 OnEventConnect() 이벤트를 처리하고
      클라이언트에도 해당 이벤트 내용을 전달합니다.


   .. py:method:: TransactionCall(self, rqname, trcode, scrno, inputs, stop_condition=None)

      TR 요청에 해당하는 RPC 입니다.

      CommRqData() 메소드 호출 이후 발생하는 OnReceiveTrData() 이벤트를 처리하고
      클라이언트에도 해당 이벤트 내용을 전달합니다.

      OnReceiveTrData() 이벤트 핸들러 함수 내부에서 요청받은 TR 에 따라 관련된 데이터를
      추가로 읽어 들인 뒤 알맞은 응답형태로 가공하여 클라이언트에 반환합니다.
      해당 과정에서 GetRepeatCnt() 및 GetCommData() 메소드를 내부적으로 호출합니다.

      경우에 따라 연속조회가 필요하다면 OnReceiveTrData() 이벤트 핸들러 함수 내부에서
      추가적인 SetInputValue() 및 CommRqData() 호출이 발생할 수 있습니다.

      일반적인 TR 이 아닌 관심종목 관련 TR 의 경우 CommRqData() 대신 CommKwRqData() 가
      내부적으로 호출됩니다.

      서버측에서 CommRqData() 혹은 CommKwRqData() 호출시 내부적으로 호출제한 회피를 위한
      대기시간이 발생할 수 있습니다.

      최초 TR 요청 이후 특정 TR 들에서는 그와 관련된 실시간 데이터가 (OpenAPI+ 레벨에서) 자동으로 등록될 수 있습니다.
      몇몇 상황에서는 해당 실시간 데이터가 유용할 수 있으나 현재 KOAPY 에서는 별도로 사용하진 않고 있으며,
      TR 에 대한 응답처리가 모두 완료된 이후에는 해당 실시간 데이터를 등록 해제하도록 처리하고 있습니다.


   .. py:method:: OrderCall(self, rqname, scrno, account, order_type, code, quantity, price, quote_type, original_order_no=None)

      주문 요청에 해당하는 RPC 입니다.

      SendOrder() 메소드 호출 이후 발생하는 OnReceiveTrData() 및 OnReceiveChejanData() 이벤트를 처리하고
      클라이언트에도 해당 이벤트 내용을 전달합니다.

      SendOrder() 메소드 호출 이후 발생하는 OnReceiveTrData() 이벤트에서
      주문번호가 확인 가능해야지만 정상주문으로 처리하고 그렇지 않다면 에러를 발생시킵니다.

      일반적으로는 OnReceiveTrData() 이벤트가 먼저 발생하고 이후 OnReceiveChejanData() 이벤트가 접수/체결/잔고확인에 각각 발생합니다.
      다만 주문건수가 폭증하는 경우 OnReceiveChejan() 이벤트가 OnReceiveTrData() 이벤트보다 앞서 수신될 수 있습니다.

      이외에 주문거부등의 케이스에서 주문거부 사유 등이 OnReceiveMsg() 이벤트로 반환됩니다.

      기본적으로 매수/매도 주문의 경우 주문받은 수량이 모두 체결될때까지 이벤트를 처리해 전달합니다.

      거래 구분:
          - 00: 지정가
          - 03: 시장가
          - 05: 조건부지정가
          - 06: 최유리지정가
          - 07: 최우선지정가
          - 10: 지정가IOC
          - 13: 시장가IOC
          - 16: 최유리IOC
          - 20: 지정가FOK
          - 23: 시장가FOK
          - 26: 최유리FOK
          - 61: 장전시간외종가
          - 62: 시간외단일가매매
          - 81: 장후시간외종가

      ※ 모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

      주문 유형:
          - 1: 신규매수
          - 2: 신규매도
          - 3: 매수취소
          - 4: 매도취소
          - 5: 매수정정
          - 6: 매도정정

      :param rqname: 사용자 구분 요청명
      :type rqname: str
      :param scrno: 화면번호 (4자리)
      :type scrno: str
      :param account: 계좌번호 (10자리)
      :type account: str
      :param order_type: 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
      :type order_type: int
      :param code: 종목코드 (6자리)
      :type code: str
      :param quantity: 주문수량
      :type quantity: int
      :param price: 주문단가
      :type price: int
      :param quote_type: 거래구분 (혹은 호가구분)
      :type quote_type: str
      :param original_order_no: 원주문번호, 신규주문에는 공백 입력, 정정/취소시 입력합니다.
      :type original_order_no: str


   .. py:method:: RealCall(self, scrno, codes, fids, opt_type=None, infer_fids=False, readable_names=False, fast_parse=False)

      실시간 데이터 요청에 해당하는 RPC 입니다.

      SetRealReg() 메소드 호출 이후 발생하는 OnReceiveRealData() 이벤트를 처리하고
      클라이언트에도 해당 이벤트 내용을 전달합니다.

      OnReceiveRealData() 이벤트 핸들러 함수 내부에서 앞서 요청받은 실시간 데이터 FID 목록 혹은
      직접 이벤트 핸들러 함수에서 확인 가능한 FID 목록에 따라 관련된 데이터를
      추가로 읽어 들인 뒤 알맞은 응답형태로 가공하여 클라이언트에 반환합니다.
      해당 과정에서 GetCommRealData() 메소드를 내부적으로 호출합니다.

      해당 RPC 는 별도의 이벤트 종료 상황이 존재하지 않기 때문에 더이상 사용하지 않는 경우
      클라이언트 측에서 해당 RPC 연결을 해제하는 식으로 더 이상 이벤트를 받지 않을 수 있습니다.
      이 경우 서버에서는 내부적으로 기 등록된 실시간 데이터에 대해 SetRealRemove() 가 호출됩니다.


   .. py:method:: LoadConditionCall(self)

      조건검색 기능 활용 이전에 먼저 조건식 목록을 불러오는데 사용할 수 있는 RPC 입니다.

      GetConditionLoad() 메소드 호출 이후 발생하는 OnReceiveConditionVer() 이벤트를 처리하고
      클라이언트에도 해당 이벤트 내용을 전달합니다.


   .. py:method:: ConditionCall(self, scrno, condition_name, condition_index, search_type, with_info=False, is_future_option=False, request_name=None)

      조건검색 기능에 해당하는 RPC 입니다.

      SendCondition() 메소드 호출 이후 발생하는 OnReceiveTrCondition() 혹은 OnReceiveRealCondition() 이벤트를
      처리하고 클라이언트에도 해당 이벤트 내용을 전달합니다.


   .. py:method:: SetLogLevel(self, level, logger='')

      서버에 존재하는 특정 로거의 로그레벨을 설정합니다.


   .. py:method:: LoadCondition(self)

      조건검색 관련 조건식을 불러옵니다.


   .. py:method:: IsConditionLoaded(self)

      조건식이 로드 되었는지 여부를 반환합니다.


   .. py:method:: EnsureConditionLoaded(self, force=False)

      조건식이 로드됨을 보장하도록 합니다.

      이미 조건식을 불러온 경우 별다른 처리를 하지 않습니다.
      조건식을 불러오지 않았다면 조건식을 불러오도록 처리합니다.


   .. py:method:: RateLimitedCommRqData(self, rqname, trcode, prevnext, scrno, inputs=None)

      CommRqData() 와 동일하지만 호출제한 회피를 위한 함수입니다.
      필요에 따라 호출제한을 회피하기 위해 실제 호출 전 대기할 수 있습니다.


   .. py:method:: RateLimitedSendCondition(self, scrno, condition_name, condition_index, search_type)

      SendCondition() 과 동일하지만 호출제한 회피를 위한 함수입니다.
      필요에 따라 호출제한을 회피하기 위해 실제 호출 전 대기할 수 있습니다.



.. py:class:: KiwoomOpenApiPlusServiceClientStubExtendedWrapper(stub, executor)

   Bases: :py:obj:`KiwoomOpenApiPlusServiceClientStubCoreWrapper`, :py:obj:`koapy.utils.logging.Logging.Logging`

   제공되는 RPC 들을 활용한 여러 사용 케이스들을 구현합니다.

   .. py:method:: GetStockBasicInfoAsDict(self, code, rqname=None, scrno=None)

      주식 종목의 기본정보를 딕셔너리 형태로 반환합니다.

      TR: OPT10001


   .. py:method:: GetStockBasicInfoAsSeries(self, code, rqname=None, scrno=None)

      주식 종목의 기본정보를 pd.Series 형태로 반환합니다.

      TR: OPT10001


   .. py:method:: GetStockQuoteInfoAsDataFrame(self, codes=None, rqname=None, scrno=None)

      복수개의 주식 종목들의 기본정보를 pd.DataFrame 형태로 반환합니다.

      TR: OPTKWFID


   .. py:method:: GetTickStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)

      틱 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

      TR: OPT10079


   .. py:method:: GetMinuteStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)

      분 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

      TR: OPT10080


   .. py:method:: GetDailyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)

      일 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

      TR: OPT10081


   .. py:method:: GetWeeklyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)

      주 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

      TR: OPT10082


   .. py:method:: GetMonthlyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)

      월 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

      TR: OPT10083


   .. py:method:: GetYearlyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)

      년 단위 차트 데이터를 pd.DataFrame 형태로 반환합니다.

      TR: OPT10094


   .. py:method:: GetDepositInfo(self, account_no, lookup_type=None, with_multi=False, rqname=None, scrno=None)

      계좌의 예수금 정보를 반환합니다.

      TR: OPW00001

      조회구분 = 3:추정조회, 2:일반조회


   .. py:method:: GetStockQuotes(self, code, rqname=None, scrno=None)

      주식의 호가정보를 반환합니다.

      TR: OPT10004


   .. py:method:: GetOrderLogAsDataFrame1(self, account_no, order_type=None, status_type=None, code=None, rqname=None, scrno=None)

      미체결 주문 정보를 반환합니다.

      TR: OPT10075

      계좌번호 = 전문 조회할 보유계좌번호
      전체종목구분 = 0:전체, 1:종목
      매매구분 = 0:전체, 1:매도, 2:매수
      종목코드 = 전문 조회할 종목코드
      체결구분 = 0:전체, 2:체결, 1:미체결


   .. py:method:: GetOrderLogAsDataFrame2(self, account_no, order_type=None, status_type=None, code=None, order_no=None, rqname=None, scrno=None)

      주문 체결 정보를 반환합니다.

      TR: OPT10076

      종목코드 = 전문 조회할 종목코드
      조회구분 = 0:전체, 1:종목
      매도수구분 = 0:전체, 1:매도, 2:매수
      계좌번호 = 전문 조회할 보유계좌번호
      비밀번호 = 사용안함(공백)
      주문번호 = 조회할 주문번호
      체결구분 = 0:전체, 2:체결, 1:미체결


   .. py:method:: GetOrderLogAsDataFrame3(self, account_no, date=None, sort_type=None, asset_type=None, order_type=None, code=None, starting_order_no=None, rqname=None, scrno=None)

      계좌별 주문 체결 내역을 반환합니다.

      TR: OPW00007

      주문일자 = YYYYMMDD (20170101 연도4자리, 월 2자리, 일 2자리 형식)
      계좌번호 = 전문 조회할 보유계좌번호
      비밀번호 = 사용안함(공백)
      비밀번호입력매체구분 = 00
      조회구분 = 1:주문순, 2:역순, 3:미체결, 4:체결내역만
      주식채권구분 = 0:전체, 1:주식, 2:채권
      매도수구분 = 0:전체, 1:매도, 2:매수
      종목코드
      시작주문번호


   .. py:method:: GetAccountRateOfReturnAsDataFrame(self, account_no, rqname=None, scrno=None)

      계좌별 수익률 정보를 반환합니다.

      TR: OPT10085


   .. py:method:: GetAccountEvaluationStatusAsSeriesAndDataFrame(self, account_no, include_delisted=True, rqname=None, scrno=None)

      계좌의 평가 현황 정보를 반환합니다.

      TR: OPW00004


   .. py:method:: GetAccountExecutionBalanceAsSeriesAndDataFrame(self, account_no, rqname=None, scrno=None)

      계좌의 체결 잔고 정보를 반환합니다.

      TR: OPW00005

      모의투자에서는 지원하지 않는 TR 입니다.


   .. py:method:: GetAccountEvaluationBalanceAsSeriesAndDataFrame(self, account_no, lookup_type=None, rqname=None, scrno=None)

      계좌의 평가 잔고 내역 정보를 반환합니다.

      TR: OPW00018

      조회구분 = 1:합산, 2:개별

      [ 주의 ]
      "수익률%" 데이터는 모의투자에서는 소숫점표현, 실거래서버에서는 소숫점으로 변환 필요 합니다.


   .. py:method:: GetMarketPriceInfo(self, code, rqname=None, scrno=None)

      종목의 시세표성 정보를 반환합니다.

      TR: OPT10007


   .. py:method:: GetRealDataForCodesAsStream(self, codes, fids=None, opt_type=None, screen_no=None, infer_fids=False, readable_names=False, fast_parse=False)

      실시간 데이터를 요청하고 스트림 형태로 반환받습니다.


   .. py:method:: GetCodeListByCondition(self, condition_name, condition_index=None, with_info=False, is_future_option=False, request_name=None, screen_no=None)

      주어진 조건식으로 조건검색을 수행하고
      검색된 종목의 종목코드를 리스트로 반환받습니다.

      파라미터 중 with_info 가 True 로 설정된 경우,
      검색된 종목들에 대한 기본 정보도 추가로 같이 반환됩니다.


   .. py:method:: GetCodeListByConditionAsStream(self, condition_name, condition_index=None, with_info=False, is_future_option=False, request_name=None, screen_no=None, old_behavior=False)

      주어진 조건식을 실시간 조건검색으로 등록합니다.
      이후 발생하는 이벤트들을 스트림 형태로 제공합니다.

      최초 검색결과는 OnReceiveTrCondition() 이벤트로 반환되며
      이후 종목의 추가/제외는 OnReceiveRealCondition() 이벤트로 반환됩니다.

      만약 with_info 가 True 로 설정된 경우,
      검색된 종목마다 추가적인 정보가 OnReceiveTrData() 이벤트를 통해 반환됩니다.



.. py:class:: KiwoomOpenApiPlusServiceClientStubWrapper(stub, executor)

   Bases: :py:obj:`KiwoomOpenApiPlusServiceClientStubExtendedWrapper`

   KiwoomOpenApiPlusServiceClientStubCoreWrapper, KiwoomOpenApiPlusServiceClientStubExtendedWrapper 의 구현 및
   KiwoomOpenApiPlusQAxWidgetUniversalMixin 의 구현들까지 최종적으로 포함된
   KiwoomOpenApiPlusServiceClientStub 객체를 위한 Mixin 래퍼 클래스 입니다.


