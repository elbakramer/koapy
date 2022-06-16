import json
import os
import queue
import subprocess

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional, Union, overload

from wrapt import synchronized

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchFunctions import (
    KiwoomOpenApiPlusDispatchFunctions,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRateLimiter import (
    KiwoomOpenApiPlusCommRqDataRateLimiter,
    KiwoomOpenApiPlusSendConditionRateLimiter,
    KiwoomOpenApiPlusSendOrderRateLimiter,
)
from koapy.backend.kiwoom_open_api_plus.utils.list_conversion import string_to_list
from koapy.config import config
from koapy.utils.ctypes import is_admin
from koapy.utils.logging import get_verbosity
from koapy.utils.logging.Logging import Logging
from koapy.utils.rate_limiting.pyside2.QRateLimitedExecutor import QRateLimitedExecutor
from koapy.utils.subprocess import Popen, function_to_subprocess_args


class KiwoomOpenApiPlusQAxWidgetUniversalMixin(KiwoomOpenApiPlusDispatchFunctions):
    """
    일차적으로 KiwoomOpenApiPlusQAxWidget 객체에 대해 사용될 수 있는 Mixin 이지만,
    넓게는 다른 KiwoomOpenApiPlusDispatchFunctions 인터페이스를 지원하는 모든 객체에서 사용될 수 있는,
    단순하면서도 유니버셜한 메소드들이 구현되어 있는 Mixin 입니다.
    """

    def IsConnected(self):
        """
        키움증권 서버에 접속되었는지 여부를 반환합니다.
        """
        return self.GetConnectState() == 1

    def ShowAccountWindow(self):
        """
        계좌 비밀번호 및 자동 로그인 처리 관련 설정창을 표시합니다.
        """
        return self.KOA_Functions("ShowAccountWindow", "")

    def GetServerGubun(self):
        """
        접속된 서버의 종류를 확인해 구분값을 반환합니다.
        """
        gubun = self.KOA_Functions("GetServerGubun", "")
        if not gubun:
            gubun = self.GetLoginInfo("GetServerGubun")
        return gubun

    def IsSimulationServer(self):
        """
        모의투자 서버 접속 여부를 확인해 반환합니다.
        """
        gubun = self.GetServerGubun()
        return gubun == "1"

    def IsRealServer(self):
        """
        실 서버 접속 여부를 확인해 반환합니다.
        """
        return not self.IsSimulationServer()

    def GetMasterStockInfo(self, code):
        """
        주식의 종목분류, 시장구분등의 정보를 제공합니다.
        """
        return self.KOA_Functions("GetMasterStockInfo", code)

    def GetMasterStockInfoAsDict(self, code):
        """
        주식의 종목분류, 시장구분등의 정보를 딕셔너리 형태로 가공하여 제공합니다.
        """
        result = self.GetMasterStockInfo(code)
        items = string_to_list(result, sep=";")
        items = [string_to_list(item, sep="|") for item in items]
        info = dict(items)
        return info

    def SetConditionSearchFlag(self, flag):
        """
        조건 검색시 동작과 관련된 플래그를 설정합니다.
        """
        return self.KOA_Functions("SetConditionSearchFlag", flag)

    def AddPriceToConditionSearchResult(self):
        """
        조건 검색시 현재가를 함께 수신하도록 설정합니다.
        """
        return self.SetConditionSearchFlag("AddPrice")

    def DelPriceFromConditionSearchResult(self):
        """
        조건 검색시 현재가를 함께 수신하지 않도록 설정합니다.
        """
        return self.SetConditionSearchFlag("DelPrice")

    def GetUpjongCode(self, code):
        """
        업종코드 목록을 반환합니다.

        인자로 사용할 수 있는 값은 0, 1, 2, 4, 7 입니다.
        0:코스피, 1: 코스닥, 2:KOSPI200, 4:KOSPI100(KOSPI50), 7:KRX100
        """
        code = str(code)
        return self.KOA_Functions("GetUpjongCode", code)

    def GetUpjongCodeAsList(self, code):
        """
        업종코드 목록을 리스트 형태로 가공하여 반환합니다.

        인자로 사용할 수 있는 값은 0, 1, 2, 4, 7 입니다.
        0:코스피, 1: 코스닥, 2:KOSPI200, 4:KOSPI100(KOSPI50), 7:KRX100
        """
        result = self.GetUpjongCode(code)
        items = string_to_list(result, sep="|")
        items = [string_to_list(item, sep=",") for item in items]
        items = [tuple(item) for item in items]
        return items

    def GetUpjongNameByCode(self, code):
        """
        주어진 업종코드의 이름을 반환합니다.
        """
        return self.KOA_Functions("GetUpjongNameByCode", code)

    def IsOrderWarningETF(self, code):
        """
        ETF 의 투자유의 종목 여부를 반환합니다.

        투자유의 종목인 경우 "1" 값이 리턴,
        그렇지 않은 경우 "0" 값 리턴.
        ETF가 아닌 종목을 입력시 "0" 값 리턴.
        """
        return self.KOA_Functions("IsOrderWarningETF", code)

    def IsOrderWarningETFAsBoolean(self, code):
        """
        ETF 의 투자유의 종목 여부를 불리언 형태로 변환하여 반환합니다.
        """
        return_code = self.IsOrderWarningETF(code)
        return_code = int(return_code)
        return_code = bool(return_code)
        return return_code

    def IsOrderWarningStock(self, code):
        """
        주식 전종목 대상 투자유의 종목 여부를 반환합니다.

        리턴 값 - "0":해당없음, "2":정리매매, "3":단기과열, "4":투자위험, "5":투자경고
        """
        return self.KOA_Functions("IsOrderWarningStock", code)

    def IsOrderWarningStockAsBoolean(self, code):
        """
        주식 전종목 대상 투자유의 종목 여부를 불리언 형태로 변환하여 반환합니다.
        """
        return_code = self.IsOrderWarningStock(code)
        return_code = int(return_code)
        return_code = bool(return_code)
        return return_code

    def GetMasterListedStockCntEx(self, code):
        """
        종목의 상장 주식수를 반환합니다.

        기존의 GetMasterListedStockCnt() 함수 사용시 발생할 수 있는 오버플로우 문제를 해결합니다.
        """
        return self.KOA_Functions("GetMasterListedStockCntEx", code)

    def GetMasterListedStockCntExAsInt(self, code):
        """
        종목의 상장 주식수를 정수 형태로 변환하여 반환합니다.
        """
        count = self.GetMasterListedStockCntEx(code)
        count = int(count)
        return count

    def GetCodeListByMarketAsList(self, market: Optional[Union[str, int]] = None):
        """
        시장의 종목 코드 목록를 리스트 형태로 가공하여 반환합니다.
        """
        if market is None:
            market = ""
        market = str(market)
        result = self.GetCodeListByMarket(market)
        result = string_to_list(result)
        return result

    def GetNameListByMarketAsList(self, market: Optional[Union[str, int]] = None):
        """
        시장의 종목 이름 목록를 리스트 형태로 가공하여 반환합니다.
        """
        codes = self.GetCodeListByMarketAsList(market)
        names = [self.GetMasterCodeName(code) for code in codes]
        return names

    def GetUserId(self):
        """
        사용자 ID 를 반환합니다.
        """
        userid = self.GetLoginInfo("USER_ID")
        return userid

    def GetUserName(self):
        """
        사용자 이름을 반환합니다.
        """
        username = self.GetLoginInfo("USER_NAME")
        return username

    def GetAccountCount(self):
        """
        계좌 개수를 반환합니다.
        """
        account_count = self.GetLoginInfo("ACCOUNT_CNT")
        account_count = int(account_count)
        return account_count

    def GetAccountList(self):
        """
        계좌 목록을 리스트 형태로 가공하여 반환합니다.
        """
        accounts = self.GetLoginInfo("ACCLIST")
        accounts = string_to_list(accounts)
        return accounts

    def GetKeyboardSecurityStatus(self):
        """
        키보드 보안 설정 상태를 반환합니다.
        """
        return self.GetLoginInfo("KEY_BSECGB")

    def IsKeyboardSecurityEnabled(self):
        """
        키보드 보안 설정 상태를 불리언 형태로 변환하여 반환합니다.
        """
        gubun = self.GetKeyboardSecurityStatus()
        return gubun == "0"

    def GetFirewallStatus(self):
        """
        방화벽 설정 상태를 반환합니다.
        """
        return self.GetLoginInfo("FIREW_SECGB")

    def IsFirewallEnabled(self):
        """
        방화벽 설정 상태를 불리언 형태로 변환하여 반환합니다.
        """
        gubun = self.GetFirewallStatus()
        return gubun == "1"

    def GetFirstAvailableAccount(self):
        """
        확인 가능한 첫번째 계좌번호를 반환합니다.
        """
        account = None
        accounts = self.GetAccountList()
        if len(accounts) > 0:
            account = accounts[0]
        return account

    def GetMasterStockStateAsList(self, code: str):
        """
        입력한 종목의 증거금 비율, 거래정지, 관리종목, 감리종목, 투자융의종목, 담보대출, 액면분할, 신용가능 여부를
        리스트 형태로 가공하여 전달합니다.
        """
        states = self.GetMasterStockState(code).strip()
        states = string_to_list(states, sep="|")
        return states

    def GetKospiCodeList(self):
        """
        장내 종목 코드 목록을 반환합니다.
        """
        codes = self.GetCodeListByMarketAsList("0")
        codes = sorted(codes)
        return codes

    def GetKosdaqCodeList(self):
        """
        코스닥 시장내 종목 코드 목록을 반환합니다.
        """
        codes = self.GetCodeListByMarketAsList("10")
        codes = sorted(codes)
        return codes

    def GetGeneralCodeList(
        self,
        include_preferred_stock: bool = False,
        include_etn: bool = False,
        include_etf: bool = False,
        include_mutual_fund: bool = False,
        include_reits: bool = False,
        include_kosdaq: bool = False,
    ):
        """
        장내 종목 코드 목록중 특정 그룹을 포함시키고 혹은 제거하고 반환합니다.
        """

        """
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
        """

        codes = self.GetKospiCodeList()

        # 코드 마지막 자리가 0 이 아니면 우선주일 가능성이 있다고 보고 제외
        if not include_preferred_stock:
            codes = [code for code in codes if code.endswith("0")]

        # 장내 시장에서 ETN 이 섞여 있는데 시장구분값으로 뺄 수가 없어서 이름을 보고 대충 제외
        if not include_etn:
            names = [self.GetMasterCodeName(code) for code in codes]
            etn_suffixes = ["ETN", "ETN(H)", "ETN B", "ETN(H) B"]
            is_not_etn_name = [
                not any(name.endswith(suffix) for suffix in etn_suffixes)
                for name in names
            ]
            codes = [code for code, cond in zip(codes, is_not_etn_name) if cond]

        # 코드값 기준 제외 준비
        codes = set(codes)

        # 나머지는 혹시나 겹치는 애들이 나올 수 있는 시장에서 코드기준 제외
        if not include_kosdaq:
            codes = codes - set(self.GetCodeListByMarketAsList("10"))  # 코스닥
        if not include_etf:
            codes = codes - set(self.GetCodeListByMarketAsList("8"))  # ETF
        if not include_mutual_fund:
            codes = codes - set(self.GetCodeListByMarketAsList("4"))  # 뮤추얼펀드
        if not include_reits:
            codes = codes - set(self.GetCodeListByMarketAsList("6"))  # 리츠

        # 정렬된 리스트 형태로 제공
        codes = sorted(list(codes))

        return codes

    def GetStockStates(self, code: str):
        """
        입력한 종목의 증거금 비율, 거래정지, 관리종목, 감리종목, 투자유의종목, 담보대출, 액면분할, 신용가능 여부를 전달합니다.
        """
        return self.GetMasterStockStateAsList(code)

    def GetSurveillanceFlag(self, code: str):
        """
        입력한 종목코드에 해당하는 종목의 감리구분을 전달합니다. (정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목)
        """
        return self.GetMasterConstruction(code)

    def IsSuspended(self, code: str):
        """
        거래정지 여부를 반환합니다.
        """
        return "거래정지" in self.GetMasterStockStateAsList(code)

    def IsUnderSurveillance(self, code: str):
        """
        감리종목 여부를 반환합니다.
        """
        return "감리종목" in self.GetMasterStockStateAsList(code)

    def IsUnderAdministration(self, code: str):
        """
        관리종목 여부를 반환합니다.
        """
        return "관리종목" in self.GetMasterStockStateAsList(code)

    def IsFlaggedForCaution(self, code: str):
        """
        감리구분이 정상이 아니거나 상태값중 투자유의종목으로 지정된 경우 참을 반환합니다.
        """
        flag = self.GetSurveillanceFlag(code)
        states = self.GetMasterStockStateAsList(code)
        flag_is_not_normal = flag != "정상"
        has_caution_state = "투자유의종목" in states
        return flag_is_not_normal or has_caution_state

    def IsNotNormal(self, code: str):
        """
        감리구분이 정상이 아니거나 상태값중 거래정지, 감리종목, 관리종목, 투자유의종목 등으로 지정된 경우 참을 반환합니다.
        """
        flag = self.GetSurveillanceFlag(code)
        states = self.GetMasterStockStateAsList(code)
        flag_is_not_normal = flag != "정상"
        bad_states = ["거래정지", "감리종목", "관리종목", "투자유의종목"]
        has_any_bad_state = any(state in states for state in bad_states)
        return flag_is_not_normal or has_any_bad_state

    def IsNormal(self, code: str):
        """
        감리구분이 정상이고 별다른 이상 상태값이 없는 경우 참을 반환합니다.
        """
        return not self.IsNotNormal(code)

    def GetConditionFilePath(self):
        """
        조건식 데이터를 로드한 후 생성되는 조건검색 관련 데이터 파일의 경로를 반환합니다.
        """
        module_path = self.GetAPIModulePath()
        module_path = Path(module_path)
        userid = self.GetUserId()
        condition_filepath = module_path / "system" / f"{userid}_NewSaveIndex.dat"
        condition_filepath = str(condition_filepath)
        return condition_filepath

    def GetConditionNameListAsList(self):
        """
        조건식 데이터를 로드한 후 확인 가능한 조건식 목록을 리스트 형태로 가공하여 반환합니다.
        """
        self.EnsureConditionLoaded()
        conditions = self.GetConditionNameList()
        conditions = string_to_list(conditions)
        conditions = [string_to_list(cond, sep="^") for cond in conditions]
        conditions = [(int(cond[0]), cond[1]) for cond in conditions]
        return conditions

    def GetAutoLoginDatPath(self):
        """
        자동 로그인 설정시 생성되는 자동 로그인 관련 데이터 파일의 경로를 반환합니다.
        """
        module_path = self.GetAPIModulePath()
        module_path = Path(module_path)
        autologin_dat = module_path / "system" / "Autologin.dat"
        autologin_dat = str(autologin_dat)
        return autologin_dat

    def IsAutoLoginEnabled(self):
        """
        자동 로그인 설정 여부를 반환합니다.

        자동 로그인 설정시 생성되는 자동 로그인 관련 데이터 파일 경로에 파일이 존재하는지의 여부를 확인합니다.
        """
        autologin_dat = self.GetAutoLoginDatPath()
        return os.path.exists(autologin_dat)

    def DisableAutoLogin(self):
        """
        자동 로그인 설정을 해제합니다.

        자동 로그인 설정시 생성되는 자동 로그인 관련 데이터 파일 경로에 파일이 존재하는 경우 해당 파일을 삭제합니다.
        """
        autologin_dat = self.GetAutoLoginDatPath()
        if os.path.exists(autologin_dat):
            os.remove(autologin_dat)

    # ======================================================================

    @classmethod
    def RunScriptInSubprocess_WithData(
        cls,
        main: Callable[..., Any],
        data: Optional[Mapping[str, Any]] = None,
        wait: bool = False,
        timeout: bool = None,
        check: bool = False,
        stdin: Optional[int] = subprocess.PIPE,
        stdout: Optional[int] = None,
    ):
        args = function_to_subprocess_args(main)
        process = Popen(args, stdin=stdin, stdout=stdout, text=True)
        json.dump(data, process.stdin)

        if wait:
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired as exc:
                process.kill()
                exc.stdout, exc.stderr = process.communicate()
                raise exc
            except:
                process.kill()
                raise
            retcode = process.poll()
            completed = subprocess.CompletedProcess(
                process.args, retcode, stdout, stderr
            )
            if check:
                completed.check_returncode()
            return completed

        return process

    @classmethod
    def LoginUsingPywinauto_Impl(cls, credentials: Optional[Mapping[str, Any]] = None):
        import pywinauto

        if credentials is None:
            credentials = config.get("koapy.backend.kiwoom_open_api_plus.credentials")

        is_in_development = False
        emulate_keyboard_input = True

        userid = credentials.get("user_id")
        password = credentials.get("user_password")
        cert = credentials.get("cert_password")

        is_save_userid = True
        is_simulation = credentials.get("is_simulation")

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        login_window = desktop.window(title="Open API Login")

        try:
            cls.logger.info("Waiting for login screen")
            timeout_login_screen_ready = 30
            login_window.wait("ready", timeout_login_screen_ready)
        except pywinauto.timings.TimeoutError:
            cls.logger.info("Cannot find login screen")
            raise
        else:
            cls.logger.info("Login screen found")
            if is_in_development:
                login_window.print_control_identifiers()

            if userid:
                cls.logger.info("Putting userid")
                if emulate_keyboard_input:
                    login_window["Edit1"].set_focus()
                    pywinauto.keyboard.send_keys(userid)
                    pywinauto.keyboard.send_keys("{TAB}")
                else:
                    login_window["Edit1"].set_text(userid)
            if password:
                cls.logger.info("Putting password")
                if emulate_keyboard_input:
                    login_window["Edit2"].set_focus()
                    pywinauto.keyboard.send_keys(password)
                    pywinauto.keyboard.send_keys("{TAB}")
                else:
                    login_window["Edit2"].set_text(password)
            else:
                raise RuntimeError("'user_password' not set, please check credentials")

            if is_save_userid:
                cls.logger.info("Checking to save userid")
                login_window["Button6"].check()  # check doesn't work
            else:
                cls.logger.info("Unchecking to save userid")
                login_window["Button6"].uncheck()  # uncheck doesn't work

            if not is_simulation:
                if not login_window["Edit3"].is_enabled():
                    cls.logger.info("Unchecking to use simulation server")
                    if emulate_keyboard_input:
                        login_window["Button5"].set_focus()
                        pywinauto.keyboard.send_keys("{SPACE}")
                    else:
                        login_window["Button5"].uncheck_by_click()

                if cert:
                    cls.logger.info("Putting cert password")
                    if emulate_keyboard_input:
                        login_window["Edit3"].set_focus()
                        pywinauto.keyboard.send_keys(cert)
                        pywinauto.keyboard.send_keys("{TAB}")
                    else:
                        login_window["Edit3"].set_text(cert)
                else:
                    raise RuntimeError(
                        "'cert_password' not set, please check credentials"
                    )
            else:
                if login_window["Edit3"].is_enabled():
                    cls.logger.info("Checking to use simulation server")
                    if emulate_keyboard_input:
                        login_window["Button5"].set_focus()
                        pywinauto.keyboard.send_keys("{SPACE}")
                    else:
                        login_window["Button5"].check_by_click()

            cls.logger.info("Logging in")
            login_window["Button1"].click()

    @classmethod
    def LoginUsingPywinauto_RunScriptInSubprocess(
        cls,
        credentials: Optional[Mapping[str, Any]] = None,
        wait: bool = False,
        timeout: bool = None,
        check: bool = False,
    ):
        def main():
            # pylint: disable=redefined-outer-name,reimported,import-self
            import json
            import sys

            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
                KiwoomOpenApiPlusQAxWidgetMixin,
            )
            from koapy.utils.logging import set_verbosity

            data = json.load(sys.stdin)
            credentials = data["credentials"]
            verbosity = data["verbosity"]
            set_verbosity(verbosity)
            KiwoomOpenApiPlusQAxWidgetMixin.LoginUsingPywinauto_Impl(credentials)

        verbosity = get_verbosity()
        data = {
            "credentials": credentials,
            "verbosity": verbosity,
        }

        return cls.RunScriptInSubprocess_WithData(
            main,
            data,
            wait=wait,
            timeout=timeout,
            check=check,
        )

    def LoginUsingPywinauto(
        self,
        credentials: Optional[Mapping[str, Any]] = None,
        wait: bool = True,
        timeout: bool = None,
        check: bool = True,
    ):
        """
        자식 프로세스 내에서 pywinauto 를 사용해 로그인 처리를 자동으로 진행합니다.
        """
        assert is_admin(), "Using pywinauto requires administrator permission"
        return self.LoginUsingPywinauto_RunScriptInSubprocess(
            credentials,
            wait=wait,
            timeout=timeout,
            check=check,
        )

    @overload
    def CommConnectAndThen(
        self,
        credentials: Mapping[str, Any],
        callback: Callable[[int], Any],
    ) -> int:
        ...

    @overload
    def CommConnectAndThen(self, credentials: Mapping[str, Any]) -> int:
        ...

    @overload
    def CommConnectAndThen(self, callback: Callable[[int], Any]) -> int:
        ...

    @overload
    def CommConnectAndThen(self) -> int:
        ...

    def CommConnectAndThen(
        self,
        credentials_or_callback=None,
        callback_or_none=None,
    ) -> int:
        """
        로그인 처리를 진행하고 이후 발생하는 이벤트 함수내에서 특정 콜백 함수를 실행합니다.
        """
        credentials = credentials_or_callback
        callback = callback_or_none

        if (
            callback is None
            and credentials is not None
            and not isinstance(credentials, dict)
            and callable(credentials)
        ):
            callback = credentials
            credentials = None

        can_use_pywinauto = is_admin()
        should_use_pywinauto = credentials is not None

        if should_use_pywinauto:
            assert (
                can_use_pywinauto
            ), "CommConnectAndThen() method requires to be run as administrator if credentials argument was given explicitly"

        if should_use_pywinauto:
            self.DisableAutoLogin()

        if credentials is None and not self.IsAutoLoginEnabled() and can_use_pywinauto:
            credentials = config.get(
                key="koapy.backend.kiwoom_open_api_plus.credentials",
                default=None,
            )
            should_use_pywinauto = credentials is not None

        def OnEventConnect(errcode):
            self.OnEventConnect.disconnect(OnEventConnect)
            if callable(callback):
                callback(errcode)

        self.OnEventConnect.connect(OnEventConnect)
        errcode = KiwoomOpenApiPlusError.try_or_raise(self.CommConnect())

        if should_use_pywinauto and not self.IsAutoLoginEnabled():
            process = self.LoginUsingPywinauto(credentials, wait=False)

        return errcode

    def Connect(self, credentials: Optional[Mapping[str, Any]] = None) -> int:
        """
        로그인 처리를 진행하고 이후 발생하는 이벤트 함수내에서 확인 가능한 에러코드 값을 반환합니다.
        """
        q = queue.Queue()

        def OnEventConnect(errcode):
            q.put(errcode)

        errcode = self.CommConnectAndThen(credentials, OnEventConnect)
        errcode = KiwoomOpenApiPlusError.try_or_raise(q.get())

        return errcode

    @overload
    def EnsureConnectedAndThen(
        self,
        credentials: Mapping[str, Any],
        callback: Callable[[int], Any],
    ) -> bool:
        ...

    @overload
    def EnsureConnectedAndThen(self, credentials: Mapping[str, Any]) -> bool:
        ...

    @overload
    def EnsureConnectedAndThen(self, callback: Callable[[int], Any]) -> bool:
        ...

    @overload
    def EnsureConnectedAndThen(self) -> bool:
        ...

    def EnsureConnectedAndThen(
        self,
        credentials_or_callback=None,
        callback_or_none=None,
    ) -> bool:
        """
        로그인 여부를 확인하고 로그인 상태를 보장한 뒤에 주어진 콜백 함수를 실행합니다.

        로그인 여부 확인시 로그인 되어있지 않다면 로그인을 진행한 뒤 주어진 콜백 함수를 실행합니다.
        이미 로그인이 되어있다면 즉시 주어진 콜백 함수를 실행합니다.
        """
        credentials = credentials_or_callback
        callback = callback_or_none

        if (
            callback is None
            and credentials is not None
            and not isinstance(credentials, dict)
            and callable(credentials)
        ):
            callback = credentials
            credentials = None

        is_connected = self.IsConnected()

        if not is_connected:

            def OnEventConnect(errcode):
                if errcode == 0:
                    if callable(callback):
                        callback(errcode)

            errcode = self.CommConnectAndThen(credentials, OnEventConnect)
        else:
            if callable(callback):
                errcode = 0
                callback(errcode)

        return is_connected

    def EnsureConnected(self, credentials: Optional[Mapping[str, Any]] = None) -> bool:
        """
        로그인 상태를 보장하도록 합니다.

        이미 로그인이 되어있는 경우 별다른 처리를 하지 않습니다.
        로그인이 되어있지 않다면 로그인을 수행합니다.
        """
        is_connected = self.IsConnected()
        if not is_connected:
            self.Connect(credentials)
            is_connected = self.IsConnected()
            assert is_connected, "Could not ensure connected"
        return is_connected

    @classmethod
    def EnableAutoLoginUsingPywinauto_Impl(
        cls, account_passwords: Optional[Mapping[str, Any]] = None
    ):
        import pywinauto

        if account_passwords is None:
            credentials = config.get("koapy.backend.kiwoom_open_api_plus.credentials")
            account_passwords = credentials.get("account_passwords")
        account_passwords = dict(account_passwords)
        
        is_in_development = False

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        account_window = desktop.window(title_re=r"계좌비밀번호 입력 \(버전: [0-9]+.+[0-9]+\)")

        try:
            cls.logger.info("Waiting for account window to show up")
            timeout_account_window_ready = 15
            account_window.wait("ready", timeout_account_window_ready)
        except pywinauto.timings.TimeoutError:
            cls.logger.info("Cannot find account window")
            raise
        else:
            cls.logger.info("Account window found")
            if is_in_development:
                account_window.print_control_identifiers()

            cls.logger.info("Enabling auto login")
            account_window["CheckBox"].check()

            account_combo = account_window["ComboBox"]
            account_cnt = account_combo.item_count()

            cls.logger.info("Putting account passwords")
            for i in range(account_cnt):
                account_combo.select(i)
                account_no = account_combo.selected_text().split()[0]
                if account_pw := account_passwords.get(account_no) or account_passwords.get("0000000000"):
                    account_window["Edit"].set_text(account_pw)
                    account_window["등록"].click()
                
            cls.logger.info("Closing account window")
            account_window["닫기"].click()

            try:
                cls.logger.info("Waiting account window to be closed")
                timeout_account_window_done = 5
                account_window.wait_not("visible", timeout_account_window_done)
            except pywinauto.timings.TimeoutError as e:
                cls.logger.info("Cannot sure account window is closed")
                raise RuntimeError("Cannot sure account window is closed") from e
            else:
                cls.logger.info("Account window closed")

    @classmethod
    def EnableAutoLoginUsingPywinauto_RunScriptInSubprocess(
        cls,
        account_passwords: Optional[Mapping[str, Any]] = None,
        wait: bool = False,
        timeout: bool = None,
        check: bool = False,
    ):
        def main():
            # pylint: disable=redefined-outer-name,reimported,import-self
            import json
            import sys

            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
                KiwoomOpenApiPlusQAxWidgetMixin,
            )
            from koapy.utils.logging import set_verbosity

            data = json.load(sys.stdin)
            account_passwords = data["account_passwords"]
            verbosity = data["verbosity"]
            set_verbosity(verbosity)
            KiwoomOpenApiPlusQAxWidgetMixin.EnableAutoLoginUsingPywinauto_Impl(
                account_passwords
            )

        verbosity = get_verbosity()
        data = {
            "account_passwords": account_passwords,
            "verbosity": verbosity,
        }

        return cls.RunScriptInSubprocess_WithData(
            main,
            data,
            wait=wait,
            timeout=timeout,
            check=check,
        )

    def EnableAutoLoginUsingPywinauto(
        self,
        credentials: Optional[Mapping[str, Any]] = None,
        wait: bool = True,
        timeout: bool = None,
        check: bool = True,
    ):
        """
        자식 프로세스 내에서 pywinauto 를 사용해 자동 로그인 설정을 자동으로 진행합니다.
        """
        assert is_admin(), "Using pywinauto requires administrator permission"
        return self.EnableAutoLoginUsingPywinauto_RunScriptInSubprocess(
            credentials,
            wait=wait,
            timeout=timeout,
            check=check,
        )

    def EnableAutoLogin(self, credentials: Optional[Mapping[str, Any]] = None):
        """
        자동 로그인을 설정합니다.
        """
        q = queue.Queue()

        def callback(errcode):
            with ThreadPoolExecutor(1) as executor:
                future = executor.submit(self.ShowAccountWindow)
                self.EnableAutoLoginUsingPywinauto(credentials)
                future.result()
                q.put(errcode)

        self.EnsureConnectedAndThen(credentials, callback)
        errcode = KiwoomOpenApiPlusError.try_or_raise(q.get())
        is_enabled = self.IsAutoLoginEnabled()
        return is_enabled

    def EnsureAutoLoginEnabled(
        self, credentials: Optional[Mapping[str, Any]] = None
    ) -> bool:
        """
        자동 로그인이 설정되어 있음을 보장하도록 합니다.

        이미 자동 로그인이 설정 되어있는 경우 별다른 처리를 하지 않습니다.
        자동 로그인이 설정되어 있지 않다면 자동 로그인을 설정을 처리합니다.
        """
        is_enabled = self.IsAutoLoginEnabled()
        if not is_enabled:
            self.EnableAutoLogin(credentials)
            is_enabled = self.IsAutoLoginEnabled()
            assert is_enabled, "Could not ensure auto login enabled"
        return is_enabled

    @classmethod
    def HandleVersionUpgradeUsingPywinauto_Impl(cls, pid):
        import psutil
        import pywinauto

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        login_window = desktop.window(title="Open API Login")

        timeout_login_successful = 4
        timeout_version_check = 1
        timeout_per_trial = timeout_login_successful + timeout_version_check

        trial_timeout = 180
        trial_count = trial_timeout / timeout_per_trial

        while trial_count > 0:
            try:
                cls.logger.info(
                    "Login in progress ... timeout after %d sec",
                    trial_count * timeout_per_trial,
                )
                trial_count -= 1
                login_window.wait_not("exists", timeout_login_successful)
                if login_window.exists():
                    # make sure that login_window control does not exist.
                    continue
            except pywinauto.timings.TimeoutError as e:
                version_window = desktop.window(title="opstarter")
                try:
                    version_window.wait("ready", timeout_version_check)
                except pywinauto.timings.TimeoutError:
                    continue
                else:
                    cls.logger.info("Version update required")

                    cls.logger.info("Closing login app")
                    login_window_proc = psutil.Process(pid)
                    login_window_proc.kill()
                    login_window_proc.wait()
                    cls.logger.info("Killed login app process")
                    timeout_login_screen_closed = 30
                    login_window.close(timeout_login_screen_closed)
                    try:
                        login_window.wait_not("visible", timeout_login_screen_closed)
                    except pywinauto.timings.TimeoutError as e:
                        cls.logger.warning("Cannot close login window")
                        raise RuntimeError("Cannot close login window") from e
                    else:
                        cls.logger.info("Closed login window")

                        cls.logger.info("Starting to update version")
                        version_window["Button"].click()

                        versionup_window = desktop.window(title="opversionup")
                        confirm_window = desktop.window(title="업그레이드 확인")

                        try:
                            cls.logger.info("Waiting for possible failure")
                            timeout_confirm_update = 10
                            versionup_window.wait("ready", timeout_confirm_update)
                        except pywinauto.timings.TimeoutError:
                            cls.logger.info("Cannot find failure confirmation popup")
                        else:
                            cls.logger.warning("Failed to update")
                            raise RuntimeError("Failed to update") from e

                        try:
                            cls.logger.info(
                                "Waiting for confirmation popup after update"
                            )
                            timeout_confirm_update = 10
                            confirm_window.wait("ready", timeout_confirm_update)
                        except pywinauto.timings.TimeoutError as e:
                            cls.logger.warning("Cannot find confirmation popup")
                            raise RuntimeError("Cannot find confirmation popup") from e
                        else:
                            cls.logger.info("Confirming update")
                            confirm_window["Button"].click()

                        cls.logger.info("Done update")
                        return True
            else:
                cls.logger.info("Login ended successfully")
                cls.logger.info("No version update required")
                return False
        return False

    @classmethod
    def HandleVersionUpgradeUsingPywinauto_RunScriptInSubprocess(
        cls,
        pid: int,
        wait: bool = False,
        timeout: bool = None,
        check: bool = False,
    ):
        def main():
            # pylint: disable=redefined-outer-name,reimported,import-self
            import json
            import sys

            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
                KiwoomOpenApiPlusQAxWidgetMixin,
            )
            from koapy.utils.logging import set_verbosity

            data = json.load(sys.stdin)
            pid = data["pid"]
            verbosity = data["verbosity"]
            set_verbosity(verbosity)
            is_updated = (
                KiwoomOpenApiPlusQAxWidgetMixin.HandleVersionUpgradeUsingPywinauto_Impl(
                    pid
                )
            )
            result = {"is_updated": is_updated}
            json.dump(result, sys.stdout)

        verbosity = get_verbosity()
        data = {
            "pid": pid,
            "verbosity": verbosity,
        }

        completed = cls.RunScriptInSubprocess_WithData(
            main,
            data,
            wait=wait,
            timeout=timeout,
            check=check,
            stdout=subprocess.PIPE,
        )
        result = json.loads(completed.stdout)
        is_updated = result["is_updated"]
        return is_updated

    def HandleVersionUpgradeUsingPywinauto(
        self,
        pid: int,
        wait: bool = True,
        timeout: bool = None,
        check: bool = True,
    ):
        """
        자식 프로세스 내에서 pywinauto 를 사용해 버전 업그레이드 처리를 자동으로 진행합니다.
        """
        assert is_admin(), "Using pywinauto requires administrator permission"
        return self.HandleVersionUpgradeUsingPywinauto_RunScriptInSubprocess(
            pid,
            wait=wait,
            timeout=timeout,
            check=check,
        )


class KiwoomOpenApiPlusQAxWidgetServerSideMixin(
    KiwoomOpenApiPlusDispatchFunctions, Logging
):
    """
    KiwoomOpenApiPlusQAxWidget 객체에 대해 Server-Side 에서만 사용되는 Mixin 입니다.

    주로 서버 환경에서만 확인하거나 처리가 가능한 아래 기능들을 커버합니다:

        - 조건검색식 로드
        - 조회 횟수 제한 회피 기능
    """

    def __init__(self):
        """
        조건검색식 로드 및 조회 횟수 제한 회피 기능 관련 초기화를 진행합니다.
        """

        """
        [OpenAPI 게시판]
          https://bbn.kiwoom.com/bbn.openAPIQnaBbsList.do

        [조회횟수 제한 관련 가이드]
          - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
          - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
          - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기
        """

        """
        [조회제한]
          OpenAPI 조회는 1초당 5회로 제한되며 복수종목 조회와 조건검색 조회 횟수가 합산됩니다.
          가령 1초 동안 시세조회2회 관심종목 1회 조건검색 2회 순서로 조회를 했다면 모두 합쳐서 5회이므로 모두 조회성공하겠지만
          조건검색을 3회 조회하면 맨 마지막 조건검색 조회는 실패하게 됩니다.

        [조건검색 제한]
          조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.
        """

        self._comm_rate_limiter = KiwoomOpenApiPlusCommRqDataRateLimiter()
        self._cond_rate_limiter = KiwoomOpenApiPlusSendConditionRateLimiter(
            self._comm_rate_limiter
        )
        self._order_rate_limiter = KiwoomOpenApiPlusSendOrderRateLimiter()

        self._comm_rate_limited_executor = QRateLimitedExecutor(
            self._comm_rate_limiter, self
        )
        self._cond_rate_limited_executor = QRateLimitedExecutor(
            self._cond_rate_limiter, self
        )
        self._order_rate_limited_executor = QRateLimitedExecutor(
            self._order_rate_limiter, self
        )

        self.RateLimitedCommRqData = self._comm_rate_limited_executor.wrap(
            self.CommRqDataWithInputs
        )
        self.RateLimitedCommKwRqData = self._comm_rate_limited_executor.wrap(
            self.CommKwRqData
        )
        self.RateLimitedSendCondition = self._cond_rate_limited_executor.wrap(
            self.SendCondition
        )
        self.RateLimitedSendOrder = self._order_rate_limited_executor.wrap(
            self.SendOrder
        )

        self._is_condition_loaded = False

        self._comm_rate_limited_executor.start()
        self._cond_rate_limited_executor.start()
        self._order_rate_limited_executor.start()

        self.destroyed.connect(self._comm_rate_limited_executor.shutdown)
        self.destroyed.connect(self._cond_rate_limited_executor.shutdown)
        self.destroyed.connect(self._order_rate_limited_executor.shutdown)

    def LoadCondition(self) -> int:
        """
        조건검색 관련 조건식을 불러옵니다.
        """
        q = queue.Queue()

        def OnReceiveConditionVer(ret, msg):
            if not ret:
                q.put(KiwoomOpenApiPlusError(msg))
            else:
                q.put((ret, msg))

        self.OnReceiveConditionVer.connect(OnReceiveConditionVer)
        try:
            return_code = KiwoomOpenApiPlusError.try_or_raise_boolean(
                self.GetConditionLoad(), "Failed to load condition"
            )
            res = q.get()
            if isinstance(res, KiwoomOpenApiPlusError):
                raise res
        except:  # pylint: disable=try-except-raise
            raise
        else:
            if return_code == 1:
                self._is_condition_loaded = True
        finally:
            self.OnReceiveConditionVer.disconnect(OnReceiveConditionVer)
        return return_code

    def IsConditionLoaded(self) -> bool:
        """
        조건식이 로드 되었는지 여부를 반환합니다.
        """
        # the original implementation of this function was like the following:
        #   condition_filepath = self.GetConditionFilePath()
        #   return os.path.exists(condition_filepath)
        # this implementation was based on the description of `GetConditionLoad()` function in the official documentation
        # which was like, "the temporary condition file would be deleted on after OCX program exits".
        # but actually it turned out that existence of this file could not guarantee that the condition is actually loaded or not
        # so here we are using entrypoint-wide member variable to remember once the condition is loaded
        return self._is_condition_loaded

    def EnsureConditionLoaded(self, force: bool = False) -> int:
        """
        조건식이 로드됨을 보장하도록 합니다.

        이미 조건식을 불러온 경우 별다른 처리를 하지 않습니다.
        조건식을 불러오지 않았다면 조건식을 불러오도록 처리합니다.
        """
        return_code = 0
        is_condition_loaded = self.IsConditionLoaded()
        if not is_condition_loaded or force:
            return_code = self.LoadCondition()
        else:
            return_code = 1
        assert return_code == 1, "Could not ensure condition loaded"
        return return_code

    def CommRqDataWithInputs(
        self,
        rqname: str,
        trcode: str,
        prevnext: Union[str, int],
        scrnno: str,
        inputs: Optional[Dict[str, str]] = None,
    ) -> int:
        """
        CommRqData() 호출 이전에 주어진 입력값을로 SetInputValue() 호출을 통한 입력값 설정을 진행합니다.
        이후 CommRqData() 를 호출합니다.
        """
        if inputs:
            for k, v in inputs.items():
                self.SetInputValue(k, v)
        prevnext = int(prevnext)  # ensure prevnext is int
        code = self.CommRqData(rqname, trcode, prevnext, scrnno)
        return code

    @synchronized
    def AtomicCommRqData(
        self,
        rqname: str,
        trcode: str,
        prevnext: Union[str, int],
        scrnno: str,
        inputs: Optional[Dict[str, str]] = None,
    ) -> int:
        """
        SetInputValue() 호출을 통한 입력값 설정 및 CommRqData() 호출을 하나의 단위로 처리할 수 있도록 Lock 을 걸고 처리합니다.
        """
        return self.CommRqDataWithInputs(rqname, trcode, prevnext, scrnno, inputs)


class KiwoomOpenApiPlusQAxWidgetMixin(
    KiwoomOpenApiPlusQAxWidgetUniversalMixin, KiwoomOpenApiPlusQAxWidgetServerSideMixin
):
    """
    KiwoomOpenApiPlusQAxWidgetUniversalMixin, KiwoomOpenApiPlusQAxWidgetServerSideMixin 구현이 포함된
    KiwoomOpenApiPlusQAxWidget 객체를 위한 Mixin 입니다.
    """
