:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin`
=================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusSimpleQAxWidgetMixin
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusComplexQAxWidgetMixin
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusQAxWidgetMixin




.. py:class:: KiwoomOpenApiPlusSimpleQAxWidgetMixin

   .. py:method:: IsConnected(self)


   .. py:method:: GetServerGubun(self)


   .. py:method:: IsSimulationServer(self)


   .. py:method:: IsRealServer(self)


   .. py:method:: ShowAccountWindow(self)


   .. py:method:: GetCodeListByMarketAsList(self, market=None)


   .. py:method:: GetNameListByMarketAsList(self, market)


   .. py:method:: GetUserId(self)


   .. py:method:: GetUserName(self)


   .. py:method:: GetAccountCount(self)


   .. py:method:: GetAccountList(self)


   .. py:method:: GetKeyboardSecurityStatus(self)


   .. py:method:: IsKeyboardSecurityEnabled(self)


   .. py:method:: GetFirewallStatus(self)


   .. py:method:: IsFirewallEnabled(self)


   .. py:method:: GetFirstAvailableAccount(self)


   .. py:method:: GetMasterStockStateAsList(self, code)


   .. py:method:: GetKospiCodeList(self)


   .. py:method:: GetKosdaqCodeList(self)


   .. py:method:: GetGeneralCodeList(self, include_preferred_stock=False, include_etn=False, include_etf=False, include_mutual_fund=False, include_reits=False, include_kosdaq=False)

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


   .. py:method:: GetStockStates(self, code)


   .. py:method:: GetSurveillanceFlag(self, code)


   .. py:method:: IsSuspended(self, code)


   .. py:method:: IsUnderSurveillance(self, code)


   .. py:method:: IsUnderAdministration(self, code)


   .. py:method:: IsFlaggedForCaution(self, code)


   .. py:method:: IsProblematic(self, code)


   .. py:method:: IsNormal(self, code)


   .. py:method:: GetConditionFilePath(self)


   .. py:method:: GetConditionNameListAsList(self)


   .. py:method:: GetAutoLoginDatPath(self)


   .. py:method:: IsAutoLoginEnabled(self)


   .. py:method:: DisableAutoLogin(self)


   .. py:method:: LoginUsingPywinauto_Impl(cls, credential=None)
      :classmethod:


   .. py:method:: LoginUsingPywinauto_RunScriptInSubprocess(cls, credential=None, wait=False, timeout=None, check=False)
      :classmethod:


   .. py:method:: LoginUsingPywinauto(self, credential=None, wait=True, timeout=None, check=True)


   .. py:method:: CommConnectAndThen(self, credential=None, callback=None)


   .. py:method:: Connect(self, credential=None)


   .. py:method:: EnsureConnectedAndThen(self, credential=None, callback=None)


   .. py:method:: EnsureConnected(self, credential=None)



.. py:class:: KiwoomOpenApiPlusComplexQAxWidgetMixin

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: LoadCondition(self)


   .. py:method:: IsConditionLoaded(self)


   .. py:method:: EnsureConditionLoaded(self, force=False)


   .. py:method:: CommRqDataWithInputs(self, rqname, trcode, prevnext, scrnno, inputs=None)


   .. py:method:: AtomicCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None)



.. py:class:: KiwoomOpenApiPlusQAxWidgetMixin

   Bases: :py:obj:`KiwoomOpenApiPlusSimpleQAxWidgetMixin`, :py:obj:`KiwoomOpenApiPlusComplexQAxWidgetMixin`


