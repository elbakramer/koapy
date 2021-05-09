:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper`
========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper.KiwoomOpenApiPlusServiceClientStubCoreWrapper
   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper.KiwoomOpenApiPlusServiceClientStubWrapper




.. class:: KiwoomOpenApiPlusServiceClientStubCoreWrapper(stub)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusSimpleQAxWidgetMixin`

   .. method:: __getattr__(self, name)


   .. method:: Call(self, name, *args)


   .. method:: LoginCall(self, credential=None)


   .. method:: TransactionCall(self, rqname, trcode, scrno, inputs, stop_condition=None)


   .. method:: OrderCall(self, rqname, scrno, account, order_type, code, quantity, price, quote_type, original_order_no=None)

      [거래구분]
        모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

        00 : 지정가
        03 : 시장가
        05 : 조건부지정가
        06 : 최유리지정가
        07 : 최우선지정가
        10 : 지정가IOC
        13 : 시장가IOC
        16 : 최유리IOC
        20 : 지정가FOK
        23 : 시장가FOK
        26 : 최유리FOK
        61 : 장전시간외종가
        62 : 시간외단일가매매
        81 : 장후시간외종가

      [주문유형]
        1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정


   .. method:: RealCall(self, scrno, codes, fids, realtype=None, infer_fids=False, readable_names=False, fast_parse=False)


   .. method:: LoadConditionCall(self)


   .. method:: ConditionCall(self, scrno, condition_name, condition_index, search_type, with_info=False, is_future_option=False, request_name=None)


   .. method:: SetLogLevel(self, level, logger='')


   .. method:: _EnsureConnectedUsingSignalConnector(self)


   .. method:: Connect(self, credential=None)


   .. method:: EnsureConnected(self, credential=None)


   .. method:: _LoadConditionUsingCall(self)


   .. method:: LoadCondition(self)


   .. method:: _EnsureConditionLoadedUsingCall(self, force=False)


   .. method:: EnsureConditionLoaded(self, force=False)


   .. method:: _RateLimitedCommRqDataUsingCall(self, rqname, trcode, prevnext, scrno, inputs=None)


   .. method:: RateLimitedCommRqData(self, rqname, trcode, prevnext, scrno, inputs=None)


   .. method:: _RateLimitedSendConditionUsingCall(self, scrno, condition_name, condition_index, search_type)


   .. method:: RateLimitedSendCondition(self, scrno, condition_name, condition_index, search_type)



.. class:: KiwoomOpenApiPlusServiceClientStubWrapper(stub)


   Bases: :py:obj:`KiwoomOpenApiPlusServiceClientStubCoreWrapper`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: _RemoveLeadingZerosForNumber(self, value, width=0)


   .. method:: _RemoveLeadingZerosForNumbersInValues(self, values, width=0)


   .. method:: _ParseTransactionCallResponses(self, responses, remove_zeros_width=None)


   .. method:: GetStockBasicInfoAsDict(self, code, rqname=None, scrno=None)


   .. method:: GetStockBasicInfoAsSeries(self, code, rqname=None, scrno=None)


   .. method:: GetStockQuoteInfoAsDataFrame(self, codes=None, rqname=None, scrno=None)


   .. method:: GetTickStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. method:: GetMinuteStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. method:: GetDailyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. method:: GetWeeklyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. method:: GetMonthlyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. method:: GetYearlyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. method:: GetDepositInfo(self, account_no, lookup_type=None, with_multi=False, rqname=None, scrno=None)

      조회구분 = 3:추정조회, 2:일반조회


   .. method:: GetStockQuotes(self, code, rqname=None, scrno=None)


   .. method:: GetOrderLogAsDataFrame1(self, account_no, order_type=None, status_type=None, code=None, rqname=None, scrno=None)

      계좌번호 = 전문 조회할 보유계좌번호
      전체종목구분 = 0:전체, 1:종목
      매매구분 = 0:전체, 1:매도, 2:매수
      종목코드 = 전문 조회할 종목코드
      체결구분 = 0:전체, 2:체결, 1:미체결


   .. method:: GetOrderLogAsDataFrame2(self, account_no, order_type=None, status_type=None, code=None, order_no=None, rqname=None, scrno=None)

      종목코드 = 전문 조회할 종목코드
      조회구분 = 0:전체, 1:종목
      매도수구분 = 0:전체, 1:매도, 2:매수
      계좌번호 = 전문 조회할 보유계좌번호
      비밀번호 = 사용안함(공백)
      주문번호 = 조회할 주문번호
      체결구분 = 0:전체, 2:체결, 1:미체결


   .. method:: GetOrderLogAsDataFrame3(self, account_no, date=None, sort_type=None, asset_type=None, order_type=None, code=None, starting_order_no=None, rqname=None, scrno=None)

      주문일자 = YYYYMMDD (20170101 연도4자리, 월 2자리, 일 2자리 형식)
      계좌번호 = 전문 조회할 보유계좌번호
      비밀번호 = 사용안함(공백)
      비밀번호입력매체구분 = 00
      조회구분 = 1:주문순, 2:역순, 3:미체결, 4:체결내역만
      주식채권구분 = 0:전체, 1:주식, 2:채권
      매도수구분 = 0:전체, 1:매도, 2:매수
      종목코드
      시작주문번호


   .. method:: GetAccountRateOfReturnAsDataFrame(self, account_no, rqname=None, scrno=None)


   .. method:: GetAccountEvaluationStatusAsSeriesAndDataFrame(self, account_no, include_delisted=True, rqname=None, scrno=None)


   .. method:: GetAccountExecutionBalanceAsSeriesAndDataFrame(self, account_no, rqname=None, scrno=None)


   .. method:: GetAccountEvaluationBalanceAsSeriesAndDataFrame(self, account_no, lookup_type=None, rqname=None, scrno=None)

      조회구분 = 1:합산, 2:개별

      [ 주의 ]
      "수익률%" 데이터는 모의투자에서는 소숫점표현, 실거래서버에서는 소숫점으로 변환 필요 합니다.


   .. method:: GetMarketPriceInfo(self, code, rqname=None, scrno=None)


   .. method:: GetRealDataForCodesAsStream(self, codes, fids=None, realtype=None, screen_no=None, infer_fids=False, readable_names=False, fast_parse=False)


   .. method:: GetCodeListByCondition(self, condition_name, condition_index=None, with_info=False, is_future_option=False, request_name=None, screen_no=None)


   .. method:: GetCodeListByConditionAsStream(self, condition_name, condition_index=None, with_info=False, is_future_option=False, request_name=None, screen_no=None)



