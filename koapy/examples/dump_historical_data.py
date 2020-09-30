import os

from koapy.data.HistoricalStockPriceDataUpdater import HistoricalStockPriceDataUpdater

codes = [
    '005930',
    '000660',
    '035420',
]
datadir = 'data'

if not os.path.exists(datadir):
    os.mkdir(datadir)

HistoricalStockPriceDataUpdater(codes, datadir, 'minute', 15).update()
