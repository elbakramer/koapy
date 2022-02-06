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

   일차적으로 KiwoomOpenApiPlusQAxWidget 객체에 대해 사용될 수 있는 Mixin 이지만,
   넓게는 다른 KiwoomOpenApiPlusDispatchFunctions 인터페이스를 지원하는 모든 객체에서 사용될 수 있는,
   단순하면서도 유니버셜한 메소드들이 구현되어 있는 Mixin 입니다.

   .. py:method:: IsConnected(self)

      키움증권 서버에 접속되었는지 여부를 반환합니다.


   .. py:method:: ShowAccountWindow(self)

      계좌 비밀번호 및 자동 로그인 처리 관련 설정창을 표시합니다.


   .. py:method:: GetServerGubun(self)

      접속된 서버의 종류를 확인해 구분값을 반환합니다.


   .. py:method:: IsSimulationServer(self)

      모의투자 서버 접속 여부를 확인해 반환합니다.


   .. py:method:: IsRealServer(self)

      실 서버 접속 여부를 확인해 반환합니다.


   .. py:method:: GetMasterStockInfo(self, code)

      주식의 종목분류, 시장구분등의 정보를 제공합니다.


   .. py:method:: GetMasterStockInfoAsDict(self, code)

      주식의 종목분류, 시장구분등의 정보를 딕셔너리 형태로 가공하여 제공합니다.


   .. py:method:: SetConditionSearchFlag(self, flag)

      조건 검색시 동작과 관련된 플래그를 설정합니다.


   .. py:method:: AddPriceToConditionSearchResult(self)

      조건 검색시 현재가를 함께 수신하도록 설정합니다.


   .. py:method:: DelPriceFromConditionSearchResult(self)

      조건 검색시 현재가를 함께 수신하지 않도록 설정합니다.


   .. py:method:: GetUpjongCode(self, code)

      업종코드 목록을 반환합니다.

      인자로 사용할 수 있는 값은 0, 1, 2, 4, 7 입니다.
      0:코스피, 1: 코스닥, 2:KOSPI200, 4:KOSPI100(KOSPI50), 7:KRX100


   .. py:method:: GetUpjongCodeAsList(self, code)

      업종코드 목록을 리스트 형태로 가공하여 반환합니다.

      인자로 사용할 수 있는 값은 0, 1, 2, 4, 7 입니다.
      0:코스피, 1: 코스닥, 2:KOSPI200, 4:KOSPI100(KOSPI50), 7:KRX100


   .. py:method:: GetUpjongNameByCode(self, code)

      주어진 업종코드의 이름을 반환합니다.


   .. py:method:: IsOrderWarningETF(self, code)

      ETF 의 투자유의 종목 여부를 반환합니다.

      투자유의 종목인 경우 "1" 값이 리턴,
      그렇지 않은 경우 "0" 값 리턴.
      ETF가 아닌 종목을 입력시 "0" 값 리턴.


   .. py:method:: IsOrderWarningETFAsBoolean(self, code)

      ETF 의 투자유의 종목 여부를 불리언 형태로 변환하여 반환합니다.


   .. py:method:: IsOrderWarningStock(self, code)

      주식 전종목 대상 투자유의 종목 여부를 반환합니다.

      리턴 값 - "0":해당없음, "2":정리매매, "3":단기과열, "4":투자위험, "5":투자경고


   .. py:method:: IsOrderWarningStockAsBoolean(self, code)

      주식 전종목 대상 투자유의 종목 여부를 불리언 형태로 변환하여 반환합니다.


   .. py:method:: GetMasterListedStockCntEx(self, code)

      종목의 상장 주식수를 반환합니다.

      기존의 GetMasterListedStockCnt() 함수 사용시 발생할 수 있는 오버플로우 문제를 해결합니다.


   .. py:method:: GetMasterListedStockCntExAsInt(self, code)

      종목의 상장 주식수를 정수 형태로 변환하여 반환합니다.


   .. py:method:: GetCodeListByMarketAsList(self, market: Optional[Union[str, int]] = None)

      시장의 종목 코드 목록를 리스트 형태로 가공하여 반환합니다.


   .. py:method:: GetNameListByMarketAsList(self, market: Optional[Union[str, int]] = None)

      시장의 종목 이름 목록를 리스트 형태로 가공하여 반환합니다.


   .. py:method:: GetUserId(self)

      사용자 ID 를 반환합니다.


   .. py:method:: GetUserName(self)

      사용자 이름을 반환합니다.


   .. py:method:: GetAccountCount(self)

      계좌 개수를 반환합니다.


   .. py:method:: GetAccountList(self)

      계좌 목록을 리스트 형태로 가공하여 반환합니다.


   .. py:method:: GetKeyboardSecurityStatus(self)

      키보드 보안 설정 상태를 반환합니다.


   .. py:method:: IsKeyboardSecurityEnabled(self)

      키보드 보안 설정 상태를 불리언 형태로 변환하여 반환합니다.


   .. py:method:: GetFirewallStatus(self)

      방화벽 설정 상태를 반환합니다.


   .. py:method:: IsFirewallEnabled(self)

      방화벽 설정 상태를 불리언 형태로 변환하여 반환합니다.


   .. py:method:: GetFirstAvailableAccount(self)

      확인 가능한 첫번째 계좌번호를 반환합니다.


   .. py:method:: GetMasterStockStateAsList(self, code: str)

      입력한 종목의 증거금 비율, 거래정지, 관리종목, 감리종목, 투자융의종목, 담보대출, 액면분할, 신용가능 여부를
      리스트 형태로 가공하여 전달합니다.


   .. py:method:: GetKospiCodeList(self)

      장내 종목 코드 목록을 반환합니다.


   .. py:method:: GetKosdaqCodeList(self)

      코스닥 시장내 종목 코드 목록을 반환합니다.


   .. py:method:: GetGeneralCodeList(self, include_preferred_stock: bool = False, include_etn: bool = False, include_etf: bool = False, include_mutual_fund: bool = False, include_reits: bool = False, include_kosdaq: bool = False)

      장내 종목 코드 목록중 특정 그룹을 포함시키고 혹은 제거하고 반환합니다.


   .. py:method:: GetStockStates(self, code: str)

      입력한 종목의 증거금 비율, 거래정지, 관리종목, 감리종목, 투자유의종목, 담보대출, 액면분할, 신용가능 여부를 전달합니다.


   .. py:method:: GetSurveillanceFlag(self, code: str)

      입력한 종목코드에 해당하는 종목의 감리구분을 전달합니다. (정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목)


   .. py:method:: IsSuspended(self, code: str)

      거래정지 여부를 반환합니다.


   .. py:method:: IsUnderSurveillance(self, code: str)

      감리종목 여부를 반환합니다.


   .. py:method:: IsUnderAdministration(self, code: str)

      관리종목 여부를 반환합니다.


   .. py:method:: IsFlaggedForCaution(self, code: str)

      감리구분이 정상이 아니거나 상태값중 투자유의종목으로 지정된 경우 참을 반환합니다.


   .. py:method:: IsNotNormal(self, code: str)

      감리구분이 정상이 아니거나 상태값중 거래정지, 감리종목, 관리종목, 투자유의종목 등으로 지정된 경우 참을 반환합니다.


   .. py:method:: IsNormal(self, code: str)

      감리구분이 정상이고 별다른 이상 상태값이 없는 경우 참을 반환합니다.


   .. py:method:: GetConditionFilePath(self)

      조건식 데이터를 로드한 후 생성되는 조건검색 관련 데이터 파일의 경로를 반환합니다.


   .. py:method:: GetConditionNameListAsList(self)

      조건식 데이터를 로드한 후 확인 가능한 조건식 목록을 리스트 형태로 가공하여 반환합니다.


   .. py:method:: GetAutoLoginDatPath(self)

      자동 로그인 설정시 생성되는 자동 로그인 관련 데이터 파일의 경로를 반환합니다.


   .. py:method:: IsAutoLoginEnabled(self)

      자동 로그인 설정 여부를 반환합니다.

      자동 로그인 설정시 생성되는 자동 로그인 관련 데이터 파일 경로에 파일이 존재하는지의 여부를 확인합니다.


   .. py:method:: DisableAutoLogin(self)

      자동 로그인 설정을 해제합니다.

      자동 로그인 설정시 생성되는 자동 로그인 관련 데이터 파일 경로에 파일이 존재하는 경우 해당 파일을 삭제합니다.


   .. py:method:: RunScriptInSubprocess_WithData(cls, main: Callable[Ellipsis, Any], data: Optional[Mapping[str, Any]] = None, wait: bool = False, timeout: bool = None, check: bool = False, stdin: Optional[int] = subprocess.PIPE, stdout: Optional[int] = None)
      :classmethod:


   .. py:method:: LoginUsingPywinauto_Impl(cls, credentials: Optional[Mapping[str, Any]] = None)
      :classmethod:


   .. py:method:: LoginUsingPywinauto_RunScriptInSubprocess(cls, credentials: Optional[Mapping[str, Any]] = None, wait: bool = False, timeout: bool = None, check: bool = False)
      :classmethod:


   .. py:method:: LoginUsingPywinauto(self, credentials: Optional[Mapping[str, Any]] = None, wait: bool = True, timeout: bool = None, check: bool = True)

      자식 프로세스 내에서 pywinauto 를 사용해 로그인 처리를 자동으로 진행합니다.


   .. py:method:: CommConnectAndThen(self, credentials: Mapping[str, Any], callback: Callable[[int], Any]) -> int
               CommConnectAndThen(self, credentials: Mapping[str, Any]) -> int
               CommConnectAndThen(self, callback: Callable[[int], Any]) -> int
               CommConnectAndThen(self) -> int

      로그인 처리를 진행하고 이후 발생하는 이벤트 함수내에서 특정 콜백 함수를 실행합니다.


   .. py:method:: Connect(self, credentials: Optional[Mapping[str, Any]] = None) -> int

      로그인 처리를 진행하고 이후 발생하는 이벤트 함수내에서 확인 가능한 에러코드 값을 반환합니다.


   .. py:method:: EnsureConnectedAndThen(self, credentials: Mapping[str, Any], callback: Callable[[int], Any]) -> bool
               EnsureConnectedAndThen(self, credentials: Mapping[str, Any]) -> bool
               EnsureConnectedAndThen(self, callback: Callable[[int], Any]) -> bool
               EnsureConnectedAndThen(self) -> bool

      로그인 여부를 확인하고 로그인 상태를 보장한 뒤에 주어진 콜백 함수를 실행합니다.

      로그인 여부 확인시 로그인 되어있지 않다면 로그인을 진행한 뒤 주어진 콜백 함수를 실행합니다.
      이미 로그인이 되어있다면 즉시 주어진 콜백 함수를 실행합니다.


   .. py:method:: EnsureConnected(self, credentials: Optional[Mapping[str, Any]] = None) -> bool

      로그인 상태를 보장하도록 합니다.

      이미 로그인이 되어있는 경우 별다른 처리를 하지 않습니다.
      로그인이 되어있지 않다면 로그인을 수행합니다.


   .. py:method:: EnableAutoLoginUsingPywinauto_Impl(cls, account_passwords: Optional[Mapping[str, Any]] = None)
      :classmethod:


   .. py:method:: EnableAutoLoginUsingPywinauto_RunScriptInSubprocess(cls, account_passwords: Optional[Mapping[str, Any]] = None, wait: bool = False, timeout: bool = None, check: bool = False)
      :classmethod:


   .. py:method:: EnableAutoLoginUsingPywinauto(self, credentials: Optional[Mapping[str, Any]] = None, wait: bool = True, timeout: bool = None, check: bool = True)

      자식 프로세스 내에서 pywinauto 를 사용해 자동 로그인 설정을 자동으로 진행합니다.


   .. py:method:: EnableAutoLogin(self, credentials: Optional[Mapping[str, Any]] = None)

      자동 로그인을 설정합니다.


   .. py:method:: EnsureAutoLoginEnabled(self, credentials: Optional[Mapping[str, Any]] = None) -> bool

      자동 로그인이 설정되어 있음을 보장하도록 합니다.

      이미 자동 로그인이 설정 되어있는 경우 별다른 처리를 하지 않습니다.
      자동 로그인이 설정되어 있지 않다면 자동 로그인을 설정을 처리합니다.


   .. py:method:: HandleVersionUpgradeUsingPywinauto_Impl(cls, pid)
      :classmethod:


   .. py:method:: HandleVersionUpgradeUsingPywinauto_RunScriptInSubprocess(cls, pid: int, wait: bool = False, timeout: bool = None, check: bool = False)
      :classmethod:


   .. py:method:: HandleVersionUpgradeUsingPywinauto(self, pid: int, wait: bool = True, timeout: bool = None, check: bool = True)

      자식 프로세스 내에서 pywinauto 를 사용해 버전 업그레이드 처리를 자동으로 진행합니다.



.. py:class:: KiwoomOpenApiPlusQAxWidgetServerSideMixin

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchFunctions.KiwoomOpenApiPlusDispatchFunctions`, :py:obj:`koapy.utils.logging.Logging.Logging`

   KiwoomOpenApiPlusQAxWidget 객체에 대해 Server-Side 에서만 사용되는 Mixin 입니다.

   주로 서버 환경에서만 확인하거나 처리가 가능한 아래 기능들을 커버합니다:

       - 조건검색식 로드
       - 조회 횟수 제한 회피 기능

   .. py:method:: LoadCondition(self) -> int

      조건검색 관련 조건식을 불러옵니다.


   .. py:method:: IsConditionLoaded(self) -> bool

      조건식이 로드 되었는지 여부를 반환합니다.


   .. py:method:: EnsureConditionLoaded(self, force: bool = False) -> int

      조건식이 로드됨을 보장하도록 합니다.

      이미 조건식을 불러온 경우 별다른 처리를 하지 않습니다.
      조건식을 불러오지 않았다면 조건식을 불러오도록 처리합니다.


   .. py:method:: CommRqDataWithInputs(self, rqname: str, trcode: str, prevnext: Union[str, int], scrnno: str, inputs: Optional[Dict[str, str]] = None) -> int

      CommRqData() 호출 이전에 주어진 입력값을로 SetInputValue() 호출을 통한 입력값 설정을 진행합니다.
      이후 CommRqData() 를 호출합니다.


   .. py:method:: AtomicCommRqData(self, rqname: str, trcode: str, prevnext: Union[str, int], scrnno: str, inputs: Optional[Dict[str, str]] = None) -> int

      SetInputValue() 호출을 통한 입력값 설정 및 CommRqData() 호출을 하나의 단위로 처리할 수 있도록 Lock 을 걸고 처리합니다.



.. py:class:: KiwoomOpenApiPlusQAxWidgetMixin

   Bases: :py:obj:`KiwoomOpenApiPlusQAxWidgetUniversalMixin`, :py:obj:`KiwoomOpenApiPlusQAxWidgetServerSideMixin`

   KiwoomOpenApiPlusQAxWidgetUniversalMixin, KiwoomOpenApiPlusQAxWidgetServerSideMixin 구현이 포함된
   KiwoomOpenApiPlusQAxWidget 객체를 위한 Mixin 입니다.


