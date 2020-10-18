import logging

import backtrader as bt

from koapy.backtrader.KiwoomOpenApiStore import KiwoomOpenApiStore
from koapy.backtrader.KiwoomOpenApiBroker import KiwoomOpenApiCommInfo
from koapy.backtrader.KrxTradingCalendar import KrxTradingCalendar

class TestStrategy(bt.Strategy):

    params = [
        ('exitbars', 5),
        ('maperiod', 15),
        ('printlog', True),
    ]

    def __init__(self):
        super().__init__()

        self.dataclose = self.datas[0].close

        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.bar_executed = 0

    def log(self, fmt, *args, doprint=False, **kwargs):
        if self.params.printlog or doprint: # pylint: disable=no-member
            dt = self.datas[0].datetime.datetime(0, naive=False)
            fmt = '%s, %s' % (dt, fmt)
            logging.info(fmt, *args, **kwargs)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('Buy Exuecuted, Size: %d, Price: %.2f, Cost: %.2f, Comm: %.2f',
                    order.executed.size,
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm)
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('Sell Executed, Size: %d, Price: %.2f, Cost: %.2f, Comm: %.2f',
                    order.executed.size,
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('Operation Profit, Gross: %.2f, Net: %.2f', trade.pnl, trade.pnlcomm)

    def next_simple(self):
        self.log('Close, %.2f', self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('Buy Create, %.2f', self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + self.params.exitbars): # pylint: disable=no-member
                self.log('Sell Create, %.2f', self.dataclose[0])
                self.order = self.sell()

    def next(self):
        return self.next_simple()

    def stop(self):
        self.log('(MA Period: %2d) Ending Value: %.2f', self.params.maperiod, self.broker.getvalue(), doprint=True) # pylint: disable=no-member

def main():
    cerebro = bt.Cerebro()

    kiwoomstore = KiwoomOpenApiStore()

    data = kiwoomstore.getdata(dataname='005930', timeframe=bt.TimeFrame.Seconds, compression=5)
    cerebro.adddata(data)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    cerebro.addtz('Asia/Seoul')
    cerebro.addcalendar(KrxTradingCalendar())

    cerebro.broker.setcash(30000000.0)
    cerebro.broker.addcommissioninfo(KiwoomOpenApiCommInfo())

    cerebro.addstrategy(TestStrategy)

    logging.info('Starting Portfolio Value: %.2f', cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
    logging.info('Final Portfolio Value: %.2f', cerebro.broker.getvalue())

if __name__ == '__main__':
    main()
