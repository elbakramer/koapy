import datetime
import logging
import subprocess
import time

import pandas as pd

from koapy.backend.daishin_cybos_plus.core.CybosPlusTypeLibSpec import INSTALLATION_PATH
from koapy.backend.daishin_cybos_plus.stub import CpSysDib, CpUtil, DsCbo1
from koapy.utils.ctypes import is_admin
from koapy.utils.itertools import chunk
from koapy.utils.logging.Logging import Logging
from koapy.utils.subprocess import function_to_subprocess_args


class CybosPlusEntrypointMixin(Logging):
    def GetConnectState(self):
        cybos: CpUtil.CpCybos = self["CpUtil.CpCybos"]
        return cybos.IsConnect

    @classmethod
    def ConnectUsingPywinauto_Impl(cls, credentials=None):
        """
        아래 구현을 참고해 작성함
        https://github.com/ippoeyeslhw/cppy/blob/master/cp_luncher.py
        """

        import pywinauto

        is_in_development = False

        if credentials is None:
            from koapy.config import config

            credentials = config.get("koapy.backend.daishin_cybos_plus.credentials")

        userid = credentials.get("user_id")
        password = credentials.get("user_password")
        cert = credentials.get("cert_password")

        auto_account_password = credentials.get("auto_account_password")
        auto_cert_password = credentials.get("auto_cert_password")
        price_check_only = credentials.get("price_check_only")

        account_passwords = credentials.get("account_passwords")

        cls.logger.info("Starting CYBOS Starter application")

        app = pywinauto.Application(allow_magic_lookup=False)
        desktop = pywinauto.Desktop(allow_magic_lookup=False)

        starter_path = INSTALLATION_PATH / "STARTER" / "ncStarter.exe"
        starter_command = f"{starter_path} /prj:cp"

        app.start(starter_command)

        from koapy.utils.pywinauto import wait_any

        ask_stop = desktop.window(title="ncStarter")
        starter = desktop.window(title="CYBOS Starter")

        def wait_ask_stop_ready():
            ask_stop.wait("ready", timeout=1)
            return 0

        def wait_starter_ready():
            starter.wait("ready", timeout=1)
            return 1

        cls.logger.info("Waiting for CYBOS Starter login screen")
        try:
            index = wait_any(
                [
                    wait_ask_stop_ready,
                    wait_starter_ready,
                ],
                timeout=30,
            )
        except pywinauto.timings.TimeoutError:
            cls.logger.exception("Failed to find login screen")
            raise
        else:
            if index == 0:
                cls.logger.info("Existing program found, shutting down")
                if is_in_development:
                    ask_stop.print_control_identifiers()
                if ask_stop["Static2"].window_text().endswith("종료하시겠습니까?"):
                    ask_stop["Button1"].click()
                    try:
                        cls.logger.info(
                            "Wating for possible failure message on shutdown"
                        )
                        ask_stop.wait_not("ready", timeout=10)
                    except pywinauto.timings.TimeoutError as err:
                        cls.logger.error("Failed to shutdown existing program")
                        if is_in_development:
                            ask_stop.print_control_identifiers()
                        if ask_stop["Static2"].window_text().endswith("종료할 수 없습니다."):
                            ask_stop["Button"].click()
                            raise RuntimeError("Cannot stop existing program") from err
                    else:
                        cls.logger.info("Successfully shutdown existing program")
                        try:
                            starter.wait("ready", timeout=30)
                        except pywinauto.timings.TimeoutError:
                            cls.logger.exception("Failed to find login screen")
                            raise
                        else:
                            cls.logger.info("CYBOS Starter login screen found")
            elif index == 1:
                cls.logger.info("CYBOS Starter login screen found")

        if is_in_development:
            starter.print_control_identifiers()

        if userid:
            cls.logger.info("Putting user id")
            starter["Edit1"].set_text(userid)
        if password:
            cls.logger.info("Putting user password")
            starter["Edit2"].set_text(password)
        else:
            raise RuntimeError("No user password given")

        if not price_check_only:
            if cert:
                cls.logger.info("Putting cert password")
                starter["Edit3"].set_text(cert)
            else:
                raise RuntimeError("No cert password given")

        if price_check_only:
            if starter["Edit3"].is_enabled():
                cls.logger.info("Checking price check only option")
                starter["Button6"].check_by_click()
        else:
            if not starter["Edit3"].is_enabled():
                starter["Button6"].uncheck_by_click()

        if auto_account_password:
            cls.logger.info("Checking auto account password option")
            starter["Button4"].check()  # check dosen't work
            try:
                confirm = desktop.window(title="대신증권")
                confirm.wait("ready", timeout=5)
            except pywinauto.timings.TimeoutError:
                pass
            else:
                if is_in_development:
                    confirm.print_control_identifiers()
                confirm["Button"].click()
        else:
            starter["Button4"].uncheck()  # uncheck dosen't work

        if auto_cert_password:
            cls.logger.info("Checking auto cert password option")
            starter["Button5"].check()  # check dosen't work
            try:
                confirm = desktop.window(title="대신증권")
                confirm.wait("ready", timeout=5)
            except pywinauto.timings.TimeoutError:
                pass
            else:
                if is_in_development:
                    confirm.print_control_identifiers()
                confirm["Button"].click()
        else:
            starter["Button5"].uncheck()  # uncheck dosen't work

        cls.logger.info("Clicking login button")
        starter["Button1"].click()

        cls.logger.info("Setting account passwords if necessary")
        should_stop = False
        while not should_stop:
            try:
                cls.logger.info("Waiting for account password setting screen")
                account_password = desktop.window(title="종합계좌 비밀번호 확인 입력")
                account_password.wait("ready", timeout=5)
            except pywinauto.timings.TimeoutError:
                cls.logger.info("Account password setting screen not found")
                should_stop = True
            else:
                cls.logger.info("Account password setting screen found")
                if is_in_development:
                    account_password.print_control_identifiers()
                account_no = (
                    account_password["Static"].window_text().split(":")[-1].strip()
                )
                if account_no in account_passwords:
                    account_password["Edit"].set_text(account_passwords[account_no])
                else:
                    raise RuntimeError(
                        "No account password given for account %s" % account_no
                    )
                account_password["Button1"].click()

        try:
            cls.logger.info("Waiting for starter screen to be closed")
            starter.wait_not("visible", timeout=60)
        except pywinauto.timings.TimeoutError:
            cls.logger.warning("Could not wait for starter screen to be closed")
        else:
            cls.logger.info("Starter screen is closed")
            try:
                cls.logger.info("Waiting for notice window")
                notice = desktop.window(title="공지사항")
                notice.wait("ready", timeout=60)
            except pywinauto.timings.TimeoutError:
                cls.logger.info("No notice window found")
            else:
                cls.logger.info("Closing notice window")
                notice.close()
                try:
                    cls.logger.info("Waiting for the notice window to be closed")
                    notice.wait_not("visible", timeout=60)
                except pywinauto.timings.TimeoutError:
                    cls.logger.warning("Could not wait for notice screen to be closed")
                else:
                    cls.logger.info("Notice window is closed")

    @classmethod
    def ConnectUsingPywinauto_RunScriptInSubprocess(cls, credentials=None):
        import json

        def main():
            import json
            import sys

            from koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypoint import (
                CybosPlusEntrypoint,
            )

            credentials = json.load(sys.stdin)
            CybosPlusEntrypoint.ConnectUsingPywinauto_Impl(credentials)

        args = function_to_subprocess_args(main)
        return subprocess.run(
            args, input=json.dumps(credentials), text=True, check=True
        )

    def ConnectUsingPywinauto(self, credentials=None):
        return self.ConnectUsingPywinauto_RunScriptInSubprocess(credentials)

    def Connect(self, credentials=None):
        assert is_admin(), "Connect() method requires to be run as administrator"

        self.ConnectUsingPywinauto(credentials)

        if self.GetConnectState() == 0:
            self.logger.error("Failed to start and connect to CYBOS Plus")
        else:
            self.logger.info("Succesfully connected to CYBOS Plus")

        return self.GetConnectState()

    def CommConnect(self, credentials=None):
        return self.Connect(credentials)

    def EnsureConnected(self, credentials=None):
        errcode = 0
        if self.GetConnectState() == 0:
            self.Connect(credentials)
        if self.GetConnectState() == 0:
            raise RuntimeError("CYBOS Plus is not running, please start CYBOS Plus")
        return errcode

    def GetCodeListByMarketAsList(self, market):
        """
        0: 구분없음
        1: 거래소
        2: 코스닥
        3: 프리보드
        4: KRX
        """
        codemgr: CpUtil.CpCodeMgr = self["CpUtil.CpCodeMgr"]
        codes = codemgr.GetStockListByMarket(market)
        codes = list(codes)
        return codes

    def GetKospiCodeList(self):
        codes = self.GetCodeListByMarketAsList(1)
        return codes

    def GetKosdaqCodeList(self):
        codes = self.GetCodeListByMarketAsList(2)
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

        codes = self.GetCodeListByMarketAsList(1)
        codemgr: CpUtil.CpCodeMgr = self["CpUtil.CpCodeMgr"]

        if not include_preferred_stock:
            codes = [code for code in codes if code.endswith("0")]
        if not include_etn:
            codes = [code for code in codes if not code.startswith("Q")]
        if not include_etf:
            codes = [
                code
                for code in codes
                if codemgr.GetStockSectionKind(code) not in [10, 12]
            ]
        if not include_mutual_fund:
            codes = [
                code for code in codes if codemgr.GetStockSectionKind(code) not in [2]
            ]
        if not include_reits:
            codes = [
                code for code in codes if codemgr.GetStockSectionKind(code) not in [3]
            ]

        if include_kosdaq:
            codes += self.GetCodeListByMarketAsList(2)

        codes = sorted(codes)

        return codes

    def GetStockDataAsDataFrame(
        self,
        code,
        chart_type,
        interval,
        start_date=None,
        end_date=None,
        adjusted_price=False,
        adjustement_only=False,
    ):
        """
        http://cybosplus.github.io/cpsysdib_rtf_1_/stockchart.htm
        """
        chart: CpSysDib.StockChart = self["CpSysDib.StockChart"]
        cybos: CpUtil.CpCybos = self["CpUtil.CpCybos"]

        needs_time = chart_type in ["m", "T"]

        if len(code) == 6 and not code.startswith("A"):
            code = "A" + code

        fids = [0]

        if needs_time:
            fids += [1]

        if not adjustement_only:
            fids += [2, 3, 4, 5, 8, 9]
        else:
            assert chart_type == "D"
            adjusted_price = True

        if adjusted_price and chart_type == "D":
            fids += [18, 19]

        sorted_fids = sorted(fids)
        field_indexes = [sorted_fids.index(i) for i in fids]

        """
        maximum_value_count = 20000
        num_fis = len(fids)
        expected_count = math.floor(maximum_value_count / num_fids) - 1
        request_count = expected_count + 1
        """

        date_format_arg = "%Y%m%d%H%M%S"
        date_format_input = "%Y%m%d"

        if start_date is not None:
            if isinstance(start_date, str):
                start_date_len = len(start_date)
                if start_date_len == 14:
                    start_date = datetime.datetime.strptime(start_date, date_format_arg)
                elif start_date_len == 8:
                    start_date = datetime.datetime.strptime(
                        start_date, date_format_input
                    )
                else:
                    raise ValueError
            if not isinstance(start_date, datetime.datetime):
                raise ValueError
            start_date = int(start_date.strftime(date_format_input))
        else:
            start_date = 0

        if end_date is not None:
            if isinstance(end_date, str):
                end_date_len = len(end_date)
                if end_date_len == 14:
                    end_date = datetime.datetime.strptime(end_date, date_format_arg)
                elif end_date_len == 8:
                    end_date = datetime.datetime.strptime(end_date, date_format_input)
                else:
                    raise ValueError
            if not isinstance(end_date, datetime.datetime):
                raise ValueError
        else:
            end_date = datetime.datetime.min

        end_date = int(end_date.strftime(date_format_input))

        chart.SetInputValue(0, code)
        chart.SetInputValue(1, ord("1"))
        chart.SetInputValue(2, start_date)
        chart.SetInputValue(3, end_date)
        chart.SetInputValue(5, fids)
        chart.SetInputValue(6, ord(chart_type))
        chart.SetInputValue(7, int(interval))
        chart.SetInputValue(9, ord("1") if adjusted_price else ord("0"))

        dataframes = []
        should_stop = False

        while not should_stop:
            limit_remain_count = cybos.GetLimitRemainCount(1)
            if limit_remain_count == 0:
                limit_remain_time_millis = cybos.GetLimitRemainTime(1)
                if limit_remain_time_millis > 0:
                    limit_remain_time_seconds = limit_remain_time_millis / 1000
                    self.logger.debug(
                        "Sleeping for %f seconds", limit_remain_time_seconds
                    )
                    time.sleep(limit_remain_time_seconds)

            chart.BlockRequest()

            records = []
            received_count = chart.GetHeaderValue(3)

            for i in range(received_count):
                record = [chart.GetDataValue(j, i) for j in field_indexes]
                records.append(record)

            names = chart.GetHeaderValue(2)
            names = [names[i] for i in field_indexes]

            df = pd.DataFrame.from_records(records, columns=names)

            if df.shape[0] > 0 and self.logger.isEnabledFor(logging.DEBUG):
                if needs_time:
                    dates = df["날짜"].astype(int).astype(str)
                    times = df["시간"].astype(int).astype(str).str.rjust(4, "0")
                    datetimes = dates.str.cat(times)
                    datetimes = pd.to_datetime(datetimes, format="%Y%m%d%H%M")
                else:
                    dates = df["날짜"].astype(int).astype(str)
                    datetimes = dates
                    datetimes = pd.to_datetime(datetimes, format="%Y%m%d")
                self.logger.debug(
                    "Received data from %s to %s for code %s",
                    datetimes.iloc[0],
                    datetimes.iloc[-1],
                    code,
                )

            should_stop = not chart.Continue

            dataframes.append(df)

        df = pd.concat(dataframes)
        df.reset_index(drop=True, inplace=True)

        return df

    def GetDailyStockDataAsDataFrame(
        self, code, start_date=None, end_date=None, adjusted_price=False
    ):
        return self.GetStockDataAsDataFrame(
            code, "D", 1, start_date, end_date, adjusted_price=adjusted_price
        )

    def GetMinuteStockDataAsDataFrame(
        self, code, interval, start_date=None, end_date=None, adjusted_price=False
    ):
        return self.GetStockDataAsDataFrame(
            code, "m", interval, start_date, end_date, adjusted_price=adjusted_price
        )

    def GetDailyAdjustmentRatioAsDataFrame(self, code, start_date=None, end_date=None):
        return self.GetStockDataAsDataFrame(
            code, "D", 1, start_date, end_date, adjustement_only=True
        )

    def GetCurrentStockDataAsDataFrame(self, codes):
        """
        http://cybosplus.github.io/cpdib_rtf_1_/stockmst2.htm
        """
        stock: DsCbo1.StockMst2 = self["DsCbo1.StockMst2"]
        cybos: CpUtil.CpCybos = self["CpUtil.CpCybos"]

        names = [
            "종목코드",
            "종목명",
            "시간",
            "현재가",
            "전일대비",
            "상태구분",
            "시가",
            "고가",
            "저가",
            "매도호가",
            "매수호가",
            "거래량",
            "거래대금",
            "총매도잔량",
            "총매수잔량",
            "매도잔량",
            "매수잔량",
            "상장주식수",
            "외국인보유비율",
            "전일종가",
            "전일거래량",
            "체결강도",
            "순간체결량",
            "체결가비교",
            "호가비교",
            "동시호가구분",
            "예상체결가",
            "예상체결가 전일대비",
            "예상체결가 상태구분",
            "예상체결가 거래량",
        ]
        fids = list(range(len(names)))

        dataframes = []
        for code_chunk in chunk(codes, 110):
            stock.SetInputValue(0, ",".join(code_chunk))

            limit_remain_count = cybos.GetLimitRemainCount(1)
            if limit_remain_count == 0:
                limit_remain_time_millis = cybos.GetLimitRemainTime(1)
                if limit_remain_time_millis > 0:
                    limit_remain_time_seconds = limit_remain_time_millis / 1000
                    self.logger.debug(
                        "Sleeping for %f seconds", limit_remain_time_seconds
                    )
                    time.sleep(limit_remain_time_seconds)

            stock.BlockRequest()

            received_count = stock.GetHeaderValue(0)
            records = []
            for i in range(received_count):
                record = [stock.GetDataValue(j, i) for j in fids]
                records.append(record)

            df = pd.DataFrame.from_records(records, columns=names)
            dataframes.append(df)

        df = pd.concat(dataframes)
        df.reset_index(drop=True, inplace=True)

        return df
