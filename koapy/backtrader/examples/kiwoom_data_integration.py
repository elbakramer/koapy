import logging

import backtrader as bt

from koapy.backtrader.KiwoomOpenApiStore import KiwoomOpenApiStore
from koapy.backtrader.KiwoomOpenApiBroker import KiwoomOpenApiCommInfo

from koapy.backtrader.examples.vanila_quickstart import OrclStrategy

def main():
    cerebro = bt.Cerebro() # pylint: disable=unexpected-keyword-arg

    kiwoomstore = KiwoomOpenApiStore()

    historial_data = kiwoomstore.getdata(dataname='005930', historical=True)
    realtime_data = kiwoomstore.getdata(dataname='005930', backfill_start=False, timeframe=bt.TimeFrame.Ticks, compression=1)

    cerebro.adddata(historial_data)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.addtz('Asia/Seoul')

    cerebro.broker.setcash(30000000.0)
    cerebro.broker.addcommissioninfo(KiwoomOpenApiCommInfo())

    cerebro.addstrategy(OrclStrategy, printlog=True)

    logging.info('Starting Portfolio Value: %.2f', cerebro.broker.getvalue())
    cerebro.run()
    logging.info('Final Portfolio Value: %.2f', cerebro.broker.getvalue())

if __name__ == '__main__':
    main()
