import os
import sys
import datetime
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d', level=logging.DEBUG)

import backtrader as bt

class OrclStrategy(bt.Strategy):

    params = [
        ('exitbars', 5),
        ('maperiod', 15),
        ('printlog', False),
    ]

    def __init__(self):
        super().__init__()

        self.dataclose = self.datas[0].close

        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.bar_executed = 0

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod) # pylint: disable=no-member

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

    def next_with_indicator(self):
        self.log('Close, %.2f', self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log('Buy Create, %.2f', self.dataclose[0])
                self.order = self.buy()

        else:
            if self.dataclose[0] < self.sma[0]:
                self.log('Sell Create, %.2f', self.dataclose[0])
                self.order = self.sell()

    def next(self):
        return self.next_with_indicator()

    def stop(self):
        self.log('(MA Period: %2d) Ending Value: %.2f', self.params.maperiod, self.broker.getvalue(), doprint=True) # pylint: disable=no-member

def main():
    cerebro = bt.Cerebro()

    _strats = cerebro.optstrategy(OrclStrategy, maperiod=range(10, 31))

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))

    # goto https://finance.yahoo.com/quote/ORCL/history and download historical data as csv
    datapath = os.path.join(modpath, 'data/orcl-1986-2020.csv')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    cerebro.adddata(data)

    cerebro.broker.setcash(100000.0)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    cerebro.broker.setcommission(commission=0.001)

    logging.info('Starting Portfolio Value: %.2f', cerebro.broker.getvalue())

    cerebro.run(maxcpus=1)

    logging.info('Final Portfolio Value: %.2f', cerebro.broker.getvalue())

if __name__ == '__main__':
    main()
