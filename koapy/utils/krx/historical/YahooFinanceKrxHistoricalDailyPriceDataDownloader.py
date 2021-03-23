import io
import requests
import pandas as pd

class YahooFinanceKrxHistoricalDailyPriceDataDownloader:

    def __init__(self):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        }

    def download(self, symbol, start_date=None, end_date=None):
        if start_date is None:
            start_date = pd.Timestamp(1980, 1, 1)
        elif not isinstance(start_date, pd.Timestamp):
            start_date = pd.Timestamp(start_date)
        if end_date is None:
            end_date = pd.Timestamp.now().normalize() + pd.Timedelta(1, unit='day')
        elif not isinstance(end_date, pd.Timestamp):
            end_date = pd.Timestamp(end_date)

        url = 'https://query1.finance.yahoo.com/v7/finance/download/%s.KS' % symbol.upper()
        params = {
            'period1': int(start_date.timestamp()),
            'period2': int(end_date.timestamp()),
            'interval': '1d',
            'events': 'history',
            'includeAdjustedClose': 'true',
        }
        response = requests.get(url, params=params, headers=self._headers)
        df = pd.read_csv(io.BytesIO(response.content), parse_dates=['Date'], index_col='Date')

        return df