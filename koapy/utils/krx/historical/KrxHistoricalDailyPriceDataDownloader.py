import requests
import pandas as pd

class KrxHistoricalDailyPriceDataDownloader:

    def __init__(self):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        }

        self._stocks = None
        self._stocks_delisted = None

        self._bld = 'dbms/MDC/STAT/standard/MDCSTAT01701'

    def get_stocks(self):
        data = {
            'mktsel': 'ALL',
            'typeNo': '0',
            'searchText': '',
            'bld': 'dbms/comm/finder/finder_stkisu',
        }
        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        response = requests.post(url, data, headers=self._headers)
        df = pd.json_normalize(response.json()['block1'])
        df = df.set_index('short_code')
        return df

    def get_stocks_delisted(self):
        data = {
            'mktsel': 'ALL',
            'searchText': '',
            'bld': 'dbms/comm/finder/finder_listdelisu',
        }
        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        response = requests.post(url, data, headers=self._headers)
        df = pd.json_normalize(response.json()['block1'])
        df = df.set_index('short_code')
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
            return self.stocks.loc[symbol]['full_code']
        if symbol in self.stocks_delisted.index:
            return self.stocks_delisted.loc[symbol]['full_code']
        raise ValueError('No full_code found for given symbol %s' % symbol)

    def download(self, symbol, start_date=None, end_date=None):
        if start_date is None:
            start_date = pd.Timestamp(1990, 1, 1)
        if end_date is None:
            end_date = pd.Timestamp.now().normalize() + pd.Timedelta(1, unit='day')

        full_code = self.get_full_code(symbol)

        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        data = {
            'bld': self._bld,
            'isuCd': full_code,
            'isuCd2': '',
            'strtDd': start_date.strftime("%Y%m%d"),
            'endDd': end_date.strftime("%Y%m%d"),
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
        }
        response = requests.post(url, data, headers=self._headers)
        df = pd.json_normalize(response.json()['output'])

        column_names = {
            'TRD_DD':'Date',
            'ISU_CD':'Code',
            'ISU_NM':'Name',
            'MKT_NM':'Market',
            'SECUGRP_NM':'SecuGroup',
            'TDD_CLSPRC':'Close',
            'FLUC_TP_CD':'UpDown',
            'CMPPRVDD_PRC':'Change',
            'FLUC_RT':'ChangeRate',
            'TDD_OPNPRC':'Open',
            'TDD_HGPRC':'High',
            'TDD_LWPRC':'Low',
            'ACC_TRDVOL':'Volume',
            'ACC_TRDVAL':'Amount',
            'MKTCAP':'MarCap',
            'CMPPREVDD_PRC': 'Change',
            'LIST_SHRS': 'Shares',
        }
        df = df.rename(columns=column_names)

        df['Date'] = pd.to_datetime(df['Date'])
        df['ChangeRate'] = pd.to_numeric(df['ChangeRate'])

        int_columns = [
            'Close',
            'UpDown',
            'Change',
            'Open',
            'High',
            'Low',
            'Volume',
            'Amount',
            'MarCap',
            'Shares'
        ]

        for col in int_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

        return df
