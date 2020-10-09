
import datetime

from backtrader.feed import DataBase
from backtrader import date2num, num2date
from backtrader.utils.py3 import queue, with_metaclass

from koapy.backtrader.KiwoomOpenApiStore import KiwoomOpenApiStore

class MetaKiwoomOpenApiData(DataBase.__class__):

    def __init__(cls, name, bases, dct): # pylint: disable=no-self-argument
        super().__init__(name, bases, dct)
        KiwoomOpenApiStore.DataCls = cls

class KiwoomOpenApiData(with_metaclass(MetaKiwoomOpenApiData, DataBase)): # pylint: disable=invalid-metaclass

    # pylint: disable=no-member

    params = (
        ('qcheck', 0.5),
        ('historical', False),  # do backfilling at the start
        ('backfill_start', True),  # do backfilling at the start
        ('backfill', True),  # do backfilling when reconnecting
        ('backfill_from', None),  # additional data source to do backfill from
        ('useask', False),
        ('reconnect', True),
        ('reconnections', -1),  # forever
        ('reconntimeout', 5.0),
    )

    _store = KiwoomOpenApiStore

    _ST_FROM, _ST_START, _ST_LIVE, _ST_HISTORBACK, _ST_OVER = range(5)

    def __init__(self, *args, **kwargs):
        self.k = self._store(*args, **kwargs)

        self.qlive = queue.Queue()
        self.qhist = queue.Queue()

        self.contractdetails = None

        self._statelivereconn = False
        self._storedmsg = dict()
        self._state = self._ST_OVER
        self._reconns = 0

    def _timeoffset(self):
        return self.k.timeoffset()

    def islive(self):
        return not self.k.historical

    def setenvironment(self, env):
        super().setenvironment(env)
        env.addstore(self.k)

    def start(self):
        super().start()

        self._statelivereconn = False
        self._storedmsg = dict()
        self._state = self._ST_OVER
        self._reconns = 0

        self.k.start(data=self)

        otf = self.k.get_granularity(self._timeframe, self._compression)

        if otf is None:
            self.put_notification(self.NOTSUPPORTED_TF)
            self._state = self._ST_OVER
            return

        self.contractdetails = cd = self.k.get_instrument(self.p.dataname)

        if cd is None:
            self.put_notification(self.NOTSUBSCRIBED)
            self._state = self._ST_OVER
            return

        if self.p.backfill_from is not None:
            self._state = self._ST_FROM
            self.p.backfill_from.setenvironment(self._env)
            self.p.backfill_from._start() # pylint: disable=protected-access
        else:
            self._start_finish()
            self._state = self._ST_START
            self._st_start()

    def _st_start(self, instart=True, timeout=None):
        if self.p.historical:
            self.put_notification(self.DELAYED)

            dtend = None
            if self.todate < float('inf'):
                dtend = num2date(self.todate)

            dtbegin = None
            if self.fromdate > float('-inf'):
                dtbegin = num2date(self.fromdate)

            self.qhist = self.k.candles(
                self.p.dataname, dtbegin, dtend,
                self._timeframe, self._compression)

            self._state = self._ST_HISTORBACK

            return True
        else:
            self.qlive = self.k.streaming_prices(self.p.dataname, timeout=timeout)

            if instart:
                self._statelivereconn = self.p.backfill_start
            else:
                self._statelivereconn = self.p.backfill

            if self._statelivereconn:
                self.put_notification(self.DELAYED)

            self._state = self._ST_LIVE

            if instart:
                self._reconns = self.p.reconnections

            return True

    def stop(self):
        super().stop()
        self.k.stop()

    def haslivedata(self):
        return bool(self._storedmsg or self.qlive)

    def _load(self):
        if self._state == self._ST_OVER:
            return False

        while True:
            if self._state == self._ST_LIVE:
                try:
                    msg = (self._storedmsg.pop(None, None) or
                           self.qlive.get(timeout=self._qcheck))
                except queue.Empty:
                    return None

                if msg is None:
                    self.put_notification(self.CONNBROKEN)

                    if not self.p.reconnect or self._reconns == 0:
                        self.put_notification(self.DISCONNECTED)
                        self._state = self._ST_OVER
                        return False

                    self._reconns -= 1
                    self._st_start(instart=False, timeout=self.p.reconntimeout)
                    continue

                if 'code' in msg:
                    self.put_notification(self.CONNBROKEN)

                    code = msg['code']

                    if code not in [599, 598, 596]:
                        self.put_notification(self.DISCONNECTED)
                        self._state = self._ST_OVER
                        return False

                    if not self.p.reconnect or self._reconns == 0:
                        self.put_notification(self.DISCONNECTED)
                        self._state = self._ST_OVER
                        return False

                    self._reconns -= 1
                    self._st_start(instart=False, timeout=self.p.reconntimeout)
                    continue

                self._reconns = self.p.reconnections

                if not self._statelivereconn:
                    if self._laststatus != self.LIVE:
                        if self.qlive.qsize() <= 1:
                            self.put_notification(self.LIVE)

                    ret = self._load_tick(msg)
                    if ret:
                        return True
                    continue

                self._storedmsg[None] = msg

                if self._laststatus != self.DELAYED:
                    self.put_notification(self.DELAYED)

                dtend = None
                if len(self) > 1:
                    dtbegin = self.datetime.datetime(-1)
                elif self.fromdate > float('-inf'):
                    dtbegin = num2date(self.fromdate)
                else:
                    dtbegin = None

                dtend = datetime.datetime.utcfromtimestamp(int(msg['time']) / 10 ** 6)

                self.qhist = self.k.candles(
                    self.p.dataname, dtbegin, dtend,
                    self._timeframe, self._compression)

                self._state = self._ST_HISTORBACK
                self._statelivereconn = False
                continue

            elif self._state == self._ST_HISTORBACK:
                msg = self.qhist.get()
                if msg is None:
                    self.put_notification(self.DISCONNECTED)
                    self._state = self._ST_OVER
                    return False

                elif 'code' in msg:
                    self.put_notification(self.NOTSUBSCRIBED)
                    self.put_notification(self.DISCONNECTED)
                    self._state = self._ST_OVER
                    return False

                if msg:
                    if self._load_history(msg):
                        return True
                    continue
                else:
                    if self.p.historical:
                        self.put_notification(self.DISCONNECTED)
                        self._state = self._ST_OVER
                        return False

                self._state = self._ST_LIVE
                continue

            elif self._state == self._ST_FROM:
                if not self.p.backfill_from.next():
                    self._state = self._ST_START
                    continue

                # copy lines of the same name
                for alias in self.lines.getlinealiases():
                    lsrc = getattr(self.p.backfill_from.lines, alias)
                    ldst = getattr(self.lines, alias)

                    ldst[0] = lsrc[0]

                return True

            elif self._state == self._ST_START:
                if not self._st_start(instart=False):
                    self._state = self._ST_OVER
                    return False

    def _load_tick(self, msg):
        dtobj = datetime.utcfromtimestamp(int(msg['time']) / 10 ** 6)
        dt = date2num(dtobj)
        if dt <= self.lines.datetime[-1]:
            return False  # time already seen

        # Common fields
        self.lines.datetime[0] = dt
        self.lines.volume[0] = 0.0
        self.lines.openinterest[0] = 0.0

        # Put the prices into the bar
        tick = float(msg['ask']) if self.p.useask else float(msg['bid'])
        self.lines.open[0] = tick
        self.lines.high[0] = tick
        self.lines.low[0] = tick
        self.lines.close[0] = tick
        self.lines.volume[0] = 0.0
        self.lines.openinterest[0] = 0.0

        return True

    def _load_history(self, msg):
        dtobj = datetime.datetime.utcfromtimestamp(int(msg['time']) / 10 ** 6)
        dt = date2num(dtobj)
        if dt <= self.lines.datetime[-1]:
            return False  # time already seen

        # Common fields
        self.lines.datetime[0] = dt
        self.lines.volume[0] = float(msg['volume'])
        self.lines.openinterest[0] = 0.0

        # Put the prices into the bar
        self.lines.open[0] = float(msg['open'])
        self.lines.high[0] = float(msg['high'])
        self.lines.low[0] = float(msg['low'])
        self.lines.close[0] = float(msg['close'])

        return True
