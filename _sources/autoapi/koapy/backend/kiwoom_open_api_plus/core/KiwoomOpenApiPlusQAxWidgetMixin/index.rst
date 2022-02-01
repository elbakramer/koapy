:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin`
=================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusQAxWidgetUniversalMixin
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusQAxWidgetServerSideMixin
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusQAxWidgetMixin




.. py:class:: KiwoomOpenApiPlusQAxWidgetUniversalMixin

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchFunctions.KiwoomOpenApiPlusDispatchFunctions`

   .. py:method:: IsConnected(self)


   .. py:method:: ShowAccountWindow(self)


   .. py:method:: GetServerGubun(self)


   .. py:method:: IsSimulationServer(self)


   .. py:method:: IsRealServer(self)


   .. py:method:: GetMasterStockInfo(self, code)


   .. py:method:: GetMasterStockInfoAsDict(self, code)


   .. py:method:: SetConditionSearchFlag(self, flag)


   .. py:method:: AddPriceToConditionSearchResult(self)


   .. py:method:: DelPriceFromConditionSearchResult(self)


   .. py:method:: GetUpjongCode(self, code)

      두번째 인자로 사용할 수 있는 값은 0, 1, 2, 4, 7 입니다.
      0:코스피, 1: 코스닥, 2:KOSPI200, 4:KOSPI100(KOSPI50), 7:KRX100


   .. py:method:: GetUpjongCodeAsList(self, code)


   .. py:method:: GetUpjongNameByCode(self, code)


   .. py:method:: IsOrderWarningETF(self, code)

      투자유의 종목인 경우 "1" 값이 리턴, 그렇지 않은 경우 "0" 값 리턴. (ETF가 아닌 종목을 입력시 "0" 값 리턴.)


   .. py:method:: IsOrderWarningETFAsBoolean(self, code)


   .. py:method:: IsOrderWarningStock(self, code)

      리턴 값 - "0":해당없음, "2":정리매매, "3":단기과열, "4":투자위험, "5":투자경고


   .. py:method:: IsOrderWarningStockAsBoolean(self, code)


   .. py:method:: GetMasterListedStockCntEx(self, code)


   .. py:method:: GetMasterListedStockCntExAsInt(self, code)


   .. py:method:: GetCodeListByMarketAsList(self, market: Optional[Union[str, int]] = None)


   .. py:method:: GetNameListByMarketAsList(self, market: Optional[Union[str, int]] = None)


   .. py:method:: GetUserId(self)


   .. py:method:: GetUserName(self)


   .. py:method:: GetAccountCount(self)


   .. py:method:: GetAccountList(self)


   .. py:method:: GetKeyboardSecurityStatus(self)


   .. py:method:: IsKeyboardSecurityEnabled(self)


   .. py:method:: GetFirewallStatus(self)


   .. py:method:: IsFirewallEnabled(self)


   .. py:method:: GetFirstAvailableAccount(self)


   .. py:method:: GetMasterStockStateAsList(self, code: str)


   .. py:method:: GetKospiCodeList(self)


   .. py:method:: GetKosdaqCodeList(self)


   .. py:method:: GetGeneralCodeList(self, include_preferred_stock: bool = False, include_etn: bool = False, include_etf: bool = False, include_mutual_fund: bool = False, include_reits: bool = False, include_kosdaq: bool = False)

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


   .. py:method:: GetStockStates(self, code: str)


   .. py:method:: GetSurveillanceFlag(self, code: str)


   .. py:method:: IsSuspended(self, code: str)


   .. py:method:: IsUnderSurveillance(self, code: str)


   .. py:method:: IsUnderAdministration(self, code: str)


   .. py:method:: IsFlaggedForCaution(self, code: str)


   .. py:method:: IsNotNormal(self, code: str)


   .. py:method:: IsNormal(self, code: str)


   .. py:method:: GetConditionFilePath(self)


   .. py:method:: GetConditionNameListAsList(self)


   .. py:method:: GetAutoLoginDatPath(self)


   .. py:method:: IsAutoLoginEnabled(self)


   .. py:method:: DisableAutoLogin(self)


   .. py:method:: LoginUsingPywinauto_Impl(cls, credentials: Optional[Mapping[str, Any]] = None)
      :classmethod:


   .. py:method:: LoginUsingPywinauto_RunScriptInSubprocess(cls, credentials: Optional[Mapping[str, Any]] = None, wait: bool = False, timeout: bool = None, check: bool = False)
      :classmethod:


   .. py:method:: LoginUsingPywinauto(self, credentials: Optional[Mapping[str, Any]] = None, wait: bool = True, timeout: bool = None, check: bool = True)


   .. py:method:: CommConnectAndThen(self, credentials: Mapping[str, Any], callback: Callable[[int], Any]) -> int
               CommConnectAndThen(self, credentials: Mapping[str, Any]) -> int
               CommConnectAndThen(self, callback: Callable[[int], Any]) -> int
               CommConnectAndThen(self) -> int


   .. py:method:: Connect(self, credentials: Optional[Mapping[str, Any]] = None) -> int


   .. py:method:: EnsureConnectedAndThen(self, credentials: Mapping[str, Any], callback: Callable[[int], Any]) -> bool
               EnsureConnectedAndThen(self, credentials: Mapping[str, Any]) -> bool
               EnsureConnectedAndThen(self, callback: Callable[[int], Any]) -> bool
               EnsureConnectedAndThen(self) -> bool


   .. py:method:: EnsureConnected(self, credentials: Optional[Mapping[str, Any]] = None) -> bool



.. py:class:: KiwoomOpenApiPlusQAxWidgetServerSideMixin

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchFunctions.KiwoomOpenApiPlusDispatchFunctions`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: LoadCondition(self) -> int


   .. py:method:: IsConditionLoaded(self) -> bool


   .. py:method:: EnsureConditionLoaded(self, force: bool = False) -> int


   .. py:method:: CommRqDataWithInputs(self, rqname: str, trcode: str, prevnext: Union[str, int], scrnno: str, inputs: Optional[Dict[str, str]] = None) -> int


   .. py:method:: AtomicCommRqData(self, rqname: str, trcode: str, prevnext: Union[str, int], scrnno: str, inputs: Optional[Dict[str, str]] = None) -> int



.. py:class:: KiwoomOpenApiPlusQAxWidgetMixin

   Bases: :py:obj:`KiwoomOpenApiPlusQAxWidgetUniversalMixin`, :py:obj:`KiwoomOpenApiPlusQAxWidgetServerSideMixin`


