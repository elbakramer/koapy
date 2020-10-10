import logging

import backtrader as bt

from koapy.backtrader.KiwoomOpenApiStore import KiwoomOpenApiStore
from koapy.backtrader.KiwoomOpenApiBroker import KiwoomOpenApiCommInfo
from koapy.backtrader.KrxTradingCalendar import KrxTradingCalendar

from koapy.backtrader.examples.vanila_quickstart import OrclStrategy

def main():
    cerebro = bt.Cerebro() # pylint: disable=unexpected-keyword-arg

    kiwoomstore = KiwoomOpenApiStore()

    data = kiwoomstore.getdata(dataname='005930', historical=True)
    cerebro.adddata(data)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    cerebro.addtz('Asia/Seoul')
    cerebro.addcalendar(KrxTradingCalendar())

    cerebro.broker.setcash(30000000.0)
    cerebro.broker.addcommissioninfo(KiwoomOpenApiCommInfo())

    # _strats = cerebro.optstrategy(OrclStrategy, maperiod=range(10, 31))
    cerebro.addstrategy(OrclStrategy, printlog=True)

    logging.info('Starting Portfolio Value: %.2f', cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
    logging.info('Final Portfolio Value: %.2f', cerebro.broker.getvalue())

if __name__ == '__main__':
    main()
