:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin`
==============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusSimpleQAxWidgetMixin
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusComplexQAxWidgetMixin
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusQAxWidgetMixin




.. class:: KiwoomOpenApiPlusSimpleQAxWidgetMixin

   .. method:: GetServerGubun(self)


   .. method:: ShowAccountWindow(self)


   .. method:: GetCodeListByMarketAsList(self, market=None)


   .. method:: GetNameListByMarketAsList(self, market)


   .. method:: GetUserId(self)


   .. method:: GetAccountList(self)


   .. method:: GetFirstAvailableAccount(self)


   .. method:: GetMasterStockStateAsList(self, code)


   .. method:: GetKospiCodeList(self)


   .. method:: GetKosdaqCodeList(self)


   .. method:: GetGeneralCodeList(self, include_preferred_stock=False, include_etn=False, include_etf=False, include_mutual_fund=False, include_reits=False, include_kosdaq=False)

      [시장구분값]
      0 : 장내
      10 : 코스닥
      3 : ELW
      8 : ETF
      50 : KONEX
      4 : 뮤추얼펀드
      5 : 신주인수권
      6 : 리츠
      9 : 하이얼펀드
      30 : K-OTC


   .. method:: IsSuspended(self, code)


   .. method:: IsInSupervision(self, code)


   .. method:: IsInSurveillance(self, code)


   .. method:: GetConditionFilePath(self)


   .. method:: GetConditionNameListAsList(self)



.. class:: KiwoomOpenApiPlusComplexQAxWidgetMixin


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: DisableAutoLogin(self)


   .. method:: LoginUsingPywinauto_Impl(cls, credential=None)
      :classmethod:


   .. method:: LoginUsingPywinauto_RunScriptInSubprocess(cls, credential=None)
      :classmethod:


   .. method:: LoginUsingPywinauto(self, credential=None)


   .. method:: Connect(self, credential=None)


   .. method:: EnsureConnected(self, credential=None)


   .. method:: IsConnected(self)


   .. method:: LoadCondition(self)


   .. method:: IsConditionLoaded(self)


   .. method:: EnsureConditionLoaded(self, force=False)


   .. method:: AtomicCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None)


   .. method:: RateLimitedCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None)

      [OpenAPI 게시판]
        https://bbn.kiwoom.com/bbn.openAPIQnaBbsList.do

      [조회횟수 제한 관련 가이드]
        - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
        - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
        - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기


   .. method:: RateLimitedCommKwRqData(self, codes, prevnext, codecnt, typeflag, rqname, scrnno)

      [조회제한]
        OpenAPI 조회는 1초당 5회로 제한되며 복수종목 조회와 조건검색 조회 횟수가 합산됩니다.
        가령 1초 동안 시세조회2회 관심종목 1회 조건검색 2회 순서로 조회를 했다면 모두 합쳐서 5회이므로 모두 조회성공하겠지만
        조건검색을 3회 조회하면 맨 마지막 조건검색 조회는 실패하게 됩니다.

      [조건검색 제한]
        조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.


   .. method:: RateLimitedCommRqDataAndCheck(self, rqname, trcode, prevnext, scrnno, inputs=None)


   .. method:: RateLimitedSendOrder(self, rqname, scrnno, accno, ordertype, code, qty, price, hogagb, orgorderno)


   .. method:: RateLimitedSendCondition(self, scrnno, condition_name, condition_index, search_type)

      [조회제한]
        OpenAPI 조회는 1초당 5회로 제한되며 복수종목 조회와 조건검색 조회 횟수가 합산됩니다.
        가령 1초 동안 시세조회2회 관심종목 1회 조건검색 2회 순서로 조회를 했다면 모두 합쳐서 5회이므로 모두 조회성공하겠지만
        조건검색을 3회 조회하면 맨 마지막 조건검색 조회는 실패하게 됩니다.

      [조건검색 제한]
        조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.



.. class:: KiwoomOpenApiPlusQAxWidgetMixin


   Bases: :py:obj:`KiwoomOpenApiPlusSimpleQAxWidgetMixin`, :py:obj:`KiwoomOpenApiPlusComplexQAxWidgetMixin`


