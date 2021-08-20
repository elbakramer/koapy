:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper`
===========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper.KiwoomOpenApiPlusServiceClientStubCoreWrapper
   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientStubWrapper.KiwoomOpenApiPlusServiceClientStubWrapper




.. py:class:: KiwoomOpenApiPlusServiceClientStubCoreWrapper(stub, executor)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusSimpleQAxWidgetMixin`

   .. py:attribute:: METHOD_NAMES
      

      

   .. py:attribute:: EVENT_NAMES
      

      

   .. py:method:: __getattr__(self, name)


   .. py:method:: Call(self, name, *args)


   .. py:method:: LoginCall(self, credential=None)


   .. py:method:: TransactionCall(self, rqname, trcode, scrno, inputs, stop_condition=None)


   .. py:method:: OrderCall(self, rqname, scrno, account, order_type, code, quantity, price, quote_type, original_order_no=None)

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


   .. py:method:: RealCall(self, scrno, codes, fids, opt_type=None, infer_fids=False, readable_names=False, fast_parse=False)


   .. py:method:: LoadConditionCall(self)


   .. py:method:: ConditionCall(self, scrno, condition_name, condition_index, search_type, with_info=False, is_future_option=False, request_name=None)


   .. py:method:: SetLogLevel(self, level, logger='')


   .. py:method:: _LoadConditionUsingCall(self)


   .. py:method:: LoadCondition(self)


   .. py:method:: _EnsureConditionLoadedUsingCall(self, force=False)


   .. py:method:: EnsureConditionLoaded(self, force=False)


   .. py:method:: _RateLimitedCommRqDataUsingCall(self, rqname, trcode, prevnext, scrno, inputs=None)


   .. py:method:: RateLimitedCommRqData(self, rqname, trcode, prevnext, scrno, inputs=None)


   .. py:method:: _RateLimitedSendConditionUsingCall(self, scrno, condition_name, condition_index, search_type)


   .. py:method:: RateLimitedSendCondition(self, scrno, condition_name, condition_index, search_type)



.. py:class:: KiwoomOpenApiPlusServiceClientStubWrapper(stub, executor)

   Bases: :py:obj:`KiwoomOpenApiPlusServiceClientStubCoreWrapper`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: _RemoveLeadingZerosForNumber(self, value, width=0)


   .. py:method:: _RemoveLeadingZerosForNumbersInValues(self, values, width=0)


   .. py:method:: _ParseTransactionCallResponses(self, responses, remove_zeros_width=None)


   .. py:method:: GetStockBasicInfoAsDict(self, code, rqname=None, scrno=None)


   .. py:method:: GetStockBasicInfoAsSeries(self, code, rqname=None, scrno=None)


   .. py:method:: GetStockQuoteInfoAsDataFrame(self, codes=None, rqname=None, scrno=None)


   .. py:method:: GetTickStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. py:method:: GetMinuteStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. py:method:: GetDailyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. py:method:: GetWeeklyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. py:method:: GetMonthlyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. py:method:: GetYearlyStockDataAsDataFrame(self, code, start_date=None, end_date=None, include_end=False, adjusted_price=False, rqname=None, scrno=None)


   .. py:method:: GetDepositInfo(self, account_no, lookup_type=None, with_multi=False, rqname=None, scrno=None)

      조회구분 = 3:추정조회, 2:일반조회


   .. py:method:: GetStockQuotes(self, code, rqname=None, scrno=None)


   .. py:method:: GetOrderLogAsDataFrame1(self, account_no, order_type=None, status_type=None, code=None, rqname=None, scrno=None)

      계좌번호 = 전문 조회할 보유계좌번호
      전체종목구분 = 0:전체, 1:종목
      매매구분 = 0:전체, 1:매도, 2:매수
      종목코드 = 전문 조회할 종목코드
      체결구분 = 0:전체, 2:체결, 1:미체결


   .. py:method:: GetOrderLogAsDataFrame2(self, account_no, order_type=None, status_type=None, code=None, order_no=None, rqname=None, scrno=None)

      종목코드 = 전문 조회할 종목코드
      조회구분 = 0:전체, 1:종목
      매도수구분 = 0:전체, 1:매도, 2:매수
      계좌번호 = 전문 조회할 보유계좌번호
      비밀번호 = 사용안함(공백)
      주문번호 = 조회할 주문번호
      체결구분 = 0:전체, 2:체결, 1:미체결


   .. py:method:: GetOrderLogAsDataFrame3(self, account_no, date=None, sort_type=None, asset_type=None, order_type=None, code=None, starting_order_no=None, rqname=None, scrno=None)

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


   .. py:method:: GetAccountEvaluationStatusAsSeriesAndDataFrame(self, account_no, include_delisted=True, rqname=None, scrno=None)


   .. py:method:: GetAccountExecutionBalanceAsSeriesAndDataFrame(self, account_no, rqname=None, scrno=None)


   .. py:method:: GetAccountEvaluationBalanceAsSeriesAndDataFrame(self, account_no, lookup_type=None, rqname=None, scrno=None)

      조회구분 = 1:합산, 2:개별

      [ 주의 ]
      "수익률%" 데이터는 모의투자에서는 소숫점표현, 실거래서버에서는 소숫점으로 변환 필요 합니다.


   .. py:method:: GetMarketPriceInfo(self, code, rqname=None, scrno=None)


   .. py:method:: GetRealDataForCodesAsStream(self, codes, fids=None, opt_type=None, screen_no=None, infer_fids=False, readable_names=False, fast_parse=False)


   .. py:method:: GetCodeListByCondition(self, condition_name, condition_index=None, with_info=False, is_future_option=False, request_name=None, screen_no=None)


   .. py:method:: _GetCodeListByConditionAsStream_GeneratorFunc(self, responses, with_info=False)


   .. py:method:: GetCodeListByConditionAsStream(self, condition_name, condition_index=None, with_info=False, is_future_option=False, request_name=None, screen_no=None, old_behavior=False)



