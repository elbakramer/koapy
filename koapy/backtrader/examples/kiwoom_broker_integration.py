import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d",
    level=logging.DEBUG,
)

import datetime

import backtrader as bt

from koapy.backtrader.KiwoomOpenApiPlusStore import KiwoomOpenApiPlusStore


class TestStrategy(bt.Strategy):

    params = [
        ("exitbars", 5),
        ("printlog", True),
    ]

    def __init__(self):
        super().__init__()

        self.dataclose = self.datas[0].close

        self.order = None
        self.order_cancel = None
        self.buyprice = None
        self.buycomm = None

        self.bar_executed = 0

    def log(self, fmt, *args, doprint=False, **kwargs):
        if self.params.printlog or doprint:  # pylint: disable=no-member
            try:
                dt = self.datas[0].datetime.datetime(0, naive=False)
            except IndexError:
                dt = datetime.datetime.now()
            fmt = "{}, {}".format(dt, fmt)
            logging.info(fmt, *args, **kwargs)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "Buy Exuecuted, Size: %d, Price: %.2f, Cost: %.2f, Comm: %.2f",
                    order.executed.size,
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm,
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(
                    "Sell Executed, Size: %d, Price: %.2f, Cost: %.2f, Comm: %.2f",
                    order.executed.size,
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm,
                )

            self.order = None
            self.bar_executed = len(self)

        elif order.status in [order.Canceled]:
            self.log("Order Canceled")
            if self.order == self.order_cancel:
                self.order = None
            self.order_cancel = None
        elif order.status in [order.Margin]:
            self.log("Order Margin")
            if self.order == self.order_cancel:
                self.order = None
            self.order_cancel = None
        elif order.status in [order.Rejected]:
            self.log("Order Rejected")
            if self.order == self.order_cancel:
                self.order = None
            self.order_cancel = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("Operation Profit, Gross: %.2f, Net: %.2f", trade.pnl, trade.pnlcomm)

    def next_market(self):
        self.log("Close, %.2f", self.dataclose[0])

        if self.order:
            return

        if not self.position:
            self.log("Buy Create, %.2f", self.dataclose[0])
            self.order = self.buy()
        else:
            if len(self) >= (
                self.bar_executed + self.params.exitbars
            ):  # pylint: disable=no-member
                self.log("Sell Create, %.2f", self.dataclose[0])
                self.order = self.sell()

    def next_limit(self):
        self.log("Close, %.2f", self.dataclose[0])

        if self.order:
            if len(self) >= (
                self.bar_executed + self.params.exitbars
            ):  # pylint: disable=no-member
                if not self.order_cancel:
                    self.log("Cancel Create")
                    self.cancel(self.order)
                    self.order_cancel = self.order
        else:
            if not self.position:
                self.log("Buy Create, %.2f", self.dataclose[0])
                self.order = self.buy(
                    exectype=bt.Order.Limit, price=self.dataclose[0] - 1000.0
                )
                self.bar_executed = len(self)
            else:
                if len(self) >= (
                    self.bar_executed + self.params.exitbars
                ):  # pylint: disable=no-member
                    self.log("No Sell Create, %.2f", self.dataclose[0])

    def start(self):
        self.log("Starting Portfolio Value: %.2f", self.broker.getvalue(), doprint=True)

    def next(self):
        return self.next_limit()

    def stop(self):
        self.log("Final Portfolio Value: %.2f", self.broker.getvalue(), doprint=True)


def main():
    cerebro = bt.Cerebro()

    kiwoomstore = KiwoomOpenApiPlusStore()
    cerebro.broker = kiwoomstore.getbroker()

    data = kiwoomstore.getdata(
        dataname="005930",
        backfill_start=False,
        timeframe=bt.TimeFrame.Ticks,
        compression=1,
    )
    cerebro.resampledata(
        data, name="005930", timeframe=bt.TimeFrame.Seconds, compression=1
    )
    cerebro.replaydata(
        data, name="005930-1day", timeframe=bt.TimeFrame.Days, compression=1
    )

    data = kiwoomstore.getdata(
        dataname="035420",
        backfill_start=False,
        timeframe=bt.TimeFrame.Ticks,
        compression=1,
    )
    cerebro.resampledata(
        data, name="035420", timeframe=bt.TimeFrame.Seconds, compression=1
    )
    cerebro.replaydata(
        data, name="035420-1day", timeframe=bt.TimeFrame.Days, compression=1
    )

    cerebro.addtz("Asia/Seoul")
    cerebro.addstrategy(TestStrategy)

    cerebro.run()


if __name__ == "__main__":
    main()
