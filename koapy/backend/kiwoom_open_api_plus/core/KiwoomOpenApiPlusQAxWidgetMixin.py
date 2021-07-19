import json
import os
import queue
import subprocess

from wrapt import synchronized

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
    KiwoomOpenApiPlusNegativeReturnCodeError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRateLimiter import (
    KiwoomOpenApiPlusCommRqDataRateLimiter,
    KiwoomOpenApiPlusSendConditionRateLimiter,
    KiwoomOpenApiPlusSendOrderRateLimiter,
)
from koapy.utils.ctypes import is_admin
from koapy.utils.logging.Logging import Logging
from koapy.utils.subprocess import function_to_subprocess_args


class KiwoomOpenApiPlusSimpleQAxWidgetMixin:
    def GetServerGubun(self):
        return self.GetLoginInfo("GetServerGubun")

    def ShowAccountWindow(self):
        return self.KOA_Functions("ShowAccountWindow", "")

    def GetCodeListByMarketAsList(self, market=None):
        if market is None:
            market = ""
        market = str(market)
        result = self.GetCodeListByMarket(market).rstrip(";")
        result = result.split(";") if result else []
        return result

    def GetNameListByMarketAsList(self, market):
        codes = self.GetCodeListByMarketAsList(market)
        names = [self.GetMasterCodeName(code) for code in codes]
        return names

    def GetUserId(self):
        userid = self.GetLoginInfo("USER_ID")
        return userid

    def GetAccountList(self):
        accounts = self.GetLoginInfo("ACCLIST").rstrip(";")
        accounts = accounts.split(";") if accounts else []
        return accounts

    def GetFirstAvailableAccount(self):
        account = None
        accounts = self.GetAccountList()
        if len(accounts) > 0:
            account = accounts[0]
        return account

    def GetMasterStockStateAsList(self, code):
        states = self.GetMasterStockState(code).strip()
        states = states.split("|") if states else []
        return states

    def GetKospiCodeList(self):
        codes = self.GetCodeListByMarketAsList("0")
        codes = sorted(codes)
        return codes

    def GetKosdaqCodeList(self):
        codes = self.GetCodeListByMarketAsList("10")
        codes = sorted(codes)
        return codes

    def GetGeneralCodeList(
        self,
        include_preferred_stock=False,
        include_etn=False,
        include_etf=False,
        include_mutual_fund=False,
        include_reits=False,
        include_kosdaq=False,
    ):
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

    def IsSuspended(self, code):
        return "거래정지" in self.GetMasterStockStateAsList(code)

    def IsInSupervision(self, code):
        return "관리종목" in self.GetMasterStockStateAsList(code)

    def IsInSurveillance(self, code):
        return "감리종목" in self.GetMasterStockStateAsList(code)

    def GetConditionFilePath(self):
        module_path = self.GetAPIModulePath()
        userid = self.GetUserId()
        condition_filepath = os.path.join(
            module_path, "system", "%s_NewSaveIndex.dat" % userid
        )
        return condition_filepath

    def GetConditionNameListAsList(self):
        self.EnsureConditionLoaded()
        conditions = self.GetConditionNameList()
        conditions = conditions.rstrip(";").split(";") if conditions else []
        conditions = [cond.split("^") for cond in conditions]
        conditions = [(int(cond[0]), cond[1]) for cond in conditions]
        return conditions


class KiwoomOpenApiPlusComplexQAxWidgetMixin(Logging):
    def __init__(self):
        self._comm_rate_limiter = KiwoomOpenApiPlusCommRqDataRateLimiter()
        self._cond_rate_limiter = KiwoomOpenApiPlusSendConditionRateLimiter(
            self._comm_rate_limiter
        )
        self._send_order_limiter = KiwoomOpenApiPlusSendOrderRateLimiter()

        self._is_condition_loaded = False

    def DisableAutoLogin(self):
        module_path = self.GetAPIModulePath()
        autologin_dat = os.path.join(module_path, "system", "Autologin.dat")
        if os.path.exists(autologin_dat):
            os.remove(autologin_dat)

    @classmethod
    def LoginUsingPywinauto_Impl(cls, credential=None):
        import pywinauto

        if credential is None:
            from koapy.config import config

            credential = config.get("koapy.backend.kiwoom_open_api_plus.credential")

        is_in_development = False
        use_set_text = False

        userid = credential.get("user_id")
        password = credential.get("user_password")
        cert = credential.get("cert_password")

        is_save_userid = True
        is_simulation = credential.get("is_simulation")

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
                if use_set_text:
                    login_window["Edit1"].set_text(userid)
                else:
                    login_window["Edit1"].set_focus()
                    pywinauto.keyboard.send_keys(userid)
                    pywinauto.keyboard.send_keys("{TAB}")
            if password:
                cls.logger.info("Putting password")
                if use_set_text:
                    login_window["Edit2"].set_text(password)
                else:
                    login_window["Edit2"].set_focus()
                    pywinauto.keyboard.send_keys(password)
                    pywinauto.keyboard.send_keys("{TAB}")
            else:
                raise RuntimeError("'user_password' not set, please check credential")

            if is_save_userid:
                cls.logger.info("Checking to save userid")
                login_window["Button6"].check()  # check doesn't work
            else:
                cls.logger.info("Unchecking to save userid")
                login_window["Button6"].uncheck()  # uncheck doesn't work

            if not is_simulation:
                if not login_window["Edit3"].is_enabled():
                    cls.logger.info("Unchecking to use simulation server")
                    login_window["Button5"].uncheck_by_click()
                if cert:
                    cls.logger.info("Putting cert password")
                    if use_set_text:
                        login_window["Edit3"].set_text(cert)
                    else:
                        login_window["Edit3"].set_focus()
                        pywinauto.keyboard.send_keys(cert)
                        pywinauto.keyboard.send_keys("{TAB}")
                else:
                    raise RuntimeError(
                        "'cert_password' not set, please check credential"
                    )
            else:
                if login_window["Edit3"].is_enabled():
                    cls.logger.info("Checking to use simulation server")
                    login_window["Button5"].check_by_click()

            cls.logger.info("Logging in")
            login_window["Button1"].click()

    @classmethod
    def LoginUsingPywinauto_RunScriptInSubprocess(cls, credential=None):
        def main():
            # pylint: disable=redefined-outer-name,reimported,import-self
            import json
            import sys

            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
                KiwoomOpenApiPlusQAxWidgetMixin,
            )

            credential = json.load(sys.stdin)
            KiwoomOpenApiPlusQAxWidgetMixin.LoginUsingPywinauto_Impl(credential)

        args = function_to_subprocess_args(main)
        return subprocess.run(args, input=json.dumps(credential), text=True, check=True)

    def LoginUsingPywinauto(self, credential=None):
        return self.LoginUsingPywinauto_RunScriptInSubprocess(credential)

    def Connect(self, credential=None):
        if credential is not None:
            assert (
                is_admin()
            ), "Connect() method requires to be run as administrator, if credential is given explicitly"
        q = queue.Queue()

        def OnEventConnect(errcode):
            q.put(errcode)

        self.OnEventConnect.connect(OnEventConnect)
        try:
            if credential is not None:
                self.DisableAutoLogin()
            errcode = KiwoomOpenApiPlusError.try_or_raise(self.CommConnect())
            if credential is not None:
                self.LoginUsingPywinauto(credential)
            errcode = KiwoomOpenApiPlusError.try_or_raise(q.get())
        finally:
            self.OnEventConnect.disconnect(OnEventConnect)
        return errcode

    def EnsureConnected(self, credential=None):
        errcode = 0  # pylint: disable=unused-variable
        status = self.GetConnectState()
        if status == 0:
            errcode = self.Connect(credential)
            status = self.GetConnectState()
        assert status == 1, "Could not ensure connected"
        return status

    def IsConnected(self):
        return self.GetConnectState() == 1

    def LoadCondition(self):
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

    def IsConditionLoaded(self):
        # the original implementation of this function was like the following:
        #   condition_filepath = self.GetConditionFilePath()
        #   return os.path.exists(condition_filepath)
        # this implementation was based on the description of `GetConditionLoad()` function in the official documentation
        # which was like, "the temporary condition file would be deleted on after OCX program exits".
        # but actually it turned out that existence of this file could not guarantee that the condition is actually loaded or not
        # so here we are using entrypoint-wide member variable to remember once the condition is loaded
        return self._is_condition_loaded

    def EnsureConditionLoaded(self, force=False):
        return_code = 0
        is_condition_loaded = self.IsConditionLoaded()
        if not is_condition_loaded or force:
            return_code = self.LoadCondition()
        else:
            return_code = 1
        assert return_code == 1, "Could not ensure condition loaded"
        return return_code

    @synchronized
    def AtomicCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None):
        if inputs:
            for k, v in inputs.items():
                self.SetInputValue(k, v)
        prevnext = int(prevnext)  # ensure prevnext is int
        code = self.CommRqData(rqname, trcode, prevnext, scrnno)
        return code

    def RateLimitedCommRqData(self, rqname, trcode, prevnext, scrnno, inputs=None):
        """
        [OpenAPI 게시판]
          https://bbn.kiwoom.com/bbn.openAPIQnaBbsList.do

        [조회횟수 제한 관련 가이드]
          - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
          - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
          - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기
        """
        self._comm_rate_limiter.sleep_if_necessary()
        return self.AtomicCommRqData(rqname, trcode, prevnext, scrnno, inputs)

    def RateLimitedCommKwRqData(
        self, codes, prevnext, codecnt, typeflag, rqname, scrnno
    ):
        """
        [조회제한]
          OpenAPI 조회는 1초당 5회로 제한되며 복수종목 조회와 조건검색 조회 횟수가 합산됩니다.
          가령 1초 동안 시세조회2회 관심종목 1회 조건검색 2회 순서로 조회를 했다면 모두 합쳐서 5회이므로 모두 조회성공하겠지만
          조건검색을 3회 조회하면 맨 마지막 조건검색 조회는 실패하게 됩니다.

        [조건검색 제한]
          조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.
        """
        self._comm_rate_limiter.sleep_if_necessary()
        return self.CommKwRqData(codes, prevnext, codecnt, typeflag, rqname, scrnno)

    def RateLimitedCommRqDataAndCheck(
        self, rqname, trcode, prevnext, scrnno, inputs=None
    ):
        code = self.RateLimitedCommRqData(rqname, trcode, prevnext, scrnno)

        spec = "CommRqData({!r}, {!r}, {!r}, {!r})".format(
            rqname, trcode, prevnext, scrnno
        )

        if inputs is not None:
            spec += " with inputs %r" % inputs

        if code == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_NONE:
            message = "CommRqData() was successful; " + spec
            self.logger.debug(message)
        elif code == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_SISE_OVERFLOW:
            message = "CommRqData() was rejected due to massive request; " + spec
            self.logger.error(message)
            raise KiwoomOpenApiPlusNegativeReturnCodeError(code)
        elif code == KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_ORD_WRONG_INPUT:
            message = (
                "CommRqData() failed due to wrong input, check if input was correctly set; "
                + spec
            )
            self.logger.error(message)
            raise KiwoomOpenApiPlusNegativeReturnCodeError(code)
        elif code in (
            KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_RQ_STRUCT_FAIL,
            KiwoomOpenApiPlusNegativeReturnCodeError.OP_ERR_RQ_STRING_FAIL,
        ):
            message = "CommRqData() request was invalid; " + spec
            self.logger.error(message)
            raise KiwoomOpenApiPlusNegativeReturnCodeError(code)
        else:
            message = "Unknown error occured during CommRqData() request; " + spec
            korean_message = (
                KiwoomOpenApiPlusNegativeReturnCodeError.get_error_message_by_code(code)
            )
            if korean_message is not None:
                message += "; Korean error message: " + korean_message
            self.logger.error(message)
            raise KiwoomOpenApiPlusNegativeReturnCodeError(code)

        return code

    def RateLimitedSendOrder(
        self, rqname, scrnno, accno, ordertype, code, qty, price, hogagb, orgorderno
    ):
        self._send_order_limiter.sleep_if_necessary()
        return self.SendOrder(
            rqname, scrnno, accno, ordertype, code, qty, price, hogagb, orgorderno
        )

    def RateLimitedSendCondition(
        self, scrnno, condition_name, condition_index, search_type
    ):
        """
        [조회제한]
          OpenAPI 조회는 1초당 5회로 제한되며 복수종목 조회와 조건검색 조회 횟수가 합산됩니다.
          가령 1초 동안 시세조회2회 관심종목 1회 조건검색 2회 순서로 조회를 했다면 모두 합쳐서 5회이므로 모두 조회성공하겠지만
          조건검색을 3회 조회하면 맨 마지막 조건검색 조회는 실패하게 됩니다.

        [조건검색 제한]
          조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.
        """
        self._cond_rate_limiter.sleep_if_necessary()
        return self.SendCondition(scrnno, condition_name, condition_index, search_type)


class KiwoomOpenApiPlusQAxWidgetMixin(
    KiwoomOpenApiPlusSimpleQAxWidgetMixin, KiwoomOpenApiPlusComplexQAxWidgetMixin
):

    pass
