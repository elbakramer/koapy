import pandas as pd
import requests

from exchange_calendars import get_calendar


class KrxHistoricalDailyPriceDataDownloader:
    def __init__(self):
        self._headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9,ko;q=0.8,fr;q=0.7,ja;q=0.6,zh-CN;q=0.5,zh;q=0.4",
            "Host": "data.krx.co.kr",
            "Origin": "http://data.krx.co.kr",
            "Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        self._stocks = None
        self._stocks_delisted = None

        self._bld = "dbms/MDC/STAT/standard/MDCSTAT01701"
        self._isuCd = ""

        self._calendar = get_calendar("XKRX")
        self._start_date = self._calendar.first_session

    def get_stocks(self):
        data = {
            "mktsel": "ALL",
            "typeNo": "0",
            "searchText": "",
            "bld": "dbms/comm/finder/finder_stkisu",
        }
        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        response = requests.post(url, data, headers=self._headers)
        df = pd.json_normalize(response.json()["block1"])
        df = df.set_index("short_code")
        return df

    def get_stocks_delisted(self):
        data = {
            "mktsel": "ALL",
            "searchText": "",
            "bld": "dbms/comm/finder/finder_listdelisu",
        }
        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        response = requests.post(url, data, headers=self._headers)
        df = pd.json_normalize(response.json()["block1"])
        df = df.set_index("short_code")
        return df

    @property
    def stocks(self):
        if self._stocks is None:
            self._stocks = self.get_stocks()
        return self._stocks

    @property
    def stocks_delisted(self):
        if self._stocks_delisted is None:
            self._stocks_delisted = self.get_stocks_delisted()
        return self._stocks_delisted

    def get_full_code(self, symbol):
        if symbol in self.stocks.index:
            return self.stocks.loc[symbol]["full_code"]
        if symbol in self.stocks_delisted.index:
            return self.stocks_delisted.loc[symbol]["full_code"]
        raise ValueError("No full_code found for given symbol %s" % symbol)

    def get_name(self, symbol):
        if symbol in self.stocks.index:
            return self.stocks.loc[symbol]["codeName"]
        if symbol in self.stocks_delisted.index:
            return self.stocks_delisted.loc[symbol]["codeName"]
        raise ValueError("No name found for given symbol %s" % symbol)

    def download(self, symbol, start_date=None, end_date=None):
        if start_date is None:
            start_date = self._start_date
        if end_date is None:
            now = pd.Timestamp.now(self._calendar.tz)
            end_date = (
                self._calendar.previous_close(now)
                .astimezone(self._calendar.tz)
                .normalize()
            )

        full_code = self.get_full_code(symbol)
        name = self.get_name(symbol)

        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        data = {
            "bld": self._bld,
            "tboxisuCd_finder_stkisu0_0": "{}/{}".format(symbol, name),
            "isuCd": full_code,
            "isuCd2": self._isuCd,
            "codeNmisuCd_finder_stkisu0_0": name,
            "param1isuCd_finder_stkisu0_0": "ALL",
            "strtDd": start_date.strftime("%Y%m%d"),
            "endDd": end_date.strftime("%Y%m%d"),
            "share": "1",
            "money": "1",
            "csvxls_isNo": "false",
        }
        self._isuCd = full_code

        response = requests.post(url, data, headers=self._headers)
        output = response.json()["output"]

        if len(output) == 0:
            return None

        df = pd.json_normalize(output)

        column_names = {
            "TRD_DD": "Date",
            "ISU_CD": "Code",
            "ISU_NM": "Name",
            "MKT_NM": "Market",
            "SECUGRP_NM": "SecuGroup",
            "TDD_CLSPRC": "Close",
            "FLUC_TP_CD": "UpDown",
            "CMPPRVDD_PRC": "Change",
            "FLUC_RT": "ChangeRate",
            "TDD_OPNPRC": "Open",
            "TDD_HGPRC": "High",
            "TDD_LWPRC": "Low",
            "ACC_TRDVOL": "Volume",
            "ACC_TRDVAL": "Amount",
            "MKTCAP": "MarCap",
            "CMPPREVDD_PRC": "Change",
            "LIST_SHRS": "Shares",
        }
        df.rename(columns=column_names, inplace=True)

        int_columns = [
            "Close",
            "UpDown",
            "Change",
            "ChangeRate",
            "Open",
            "High",
            "Low",
            "Volume",
            "Amount",
            "MarCap",
            "Shares",
        ]

        for col in int_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].str.replace(",", ""), errors="coerce")

        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)

        return df
