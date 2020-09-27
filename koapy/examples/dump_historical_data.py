import os

from koapy.data.HistoricalStockPriceDataUpdater import Historical15MinuteStockPriceDataToExcelUpdater

codes = [
    '005930',
    '000660',
    '035420',
]
datadir = 'data'

if not os.path.exists(datadir):
    os.mkdir(datadir)

Historical15MinuteStockPriceDataToExcelUpdater(codes, datadir).update()
