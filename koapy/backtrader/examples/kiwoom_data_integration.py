import logging

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d",
    level=logging.DEBUG,
)

import backtrader as bt

from koapy.backtrader.examples.vanila_quickstart import OrclStrategy
from koapy.backtrader.KiwoomOpenApiPlusBroker import KiwoomOpenApiPlusCommInfo
from koapy.backtrader.KiwoomOpenApiPlusStore import KiwoomOpenApiPlusStore


def main():
    logging.info("Creating Cerebro")
    cerebro = bt.Cerebro()  # pylint: disable=unexpected-keyword-arg

    logging.info("Initializing Kiwoom Store")
    kiwoomstore = KiwoomOpenApiPlusStore()

    logging.info("Getting data")
    historial_data = kiwoomstore.getdata(dataname="005930", historical=True)
    realtime_data = kiwoomstore.getdata(
        dataname="005930",
        backfill_start=False,
        timeframe=bt.TimeFrame.Ticks,
        compression=1,
    )

    logging.info("Adding data")
    cerebro.adddata(historial_data)

    logging.info("Configuring others")
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.addtz("Asia/Seoul")

    cerebro.broker.setcash(30000000.0)
    cerebro.broker.addcommissioninfo(KiwoomOpenApiPlusCommInfo())

    logging.info("Setting strategy")
    cerebro.addstrategy(OrclStrategy, printlog=True)

    logging.info("Starting Portfolio Value: %.2f", cerebro.broker.getvalue())
    cerebro.run()
    logging.info("Final Portfolio Value: %.2f", cerebro.broker.getvalue())


if __name__ == "__main__":
    main()
