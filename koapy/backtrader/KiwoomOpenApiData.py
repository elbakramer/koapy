import datetime
import logging

from pytz import utc

from backtrader import date2num, num2date
from backtrader.feed import DataBase
from backtrader.utils.py3 import queue, with_metaclass

from koapy.backtrader.KiwoomOpenApiStore import KiwoomOpenApiStore

class MetaKiwoomOpenApiData(DataBase.__class__):

    def __init__(cls, name, bases, dct): # pylint: disable=no-self-argument
        super(MetaKiwoomOpenApiData, cls).__init__(name, bases, dct)
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
        ('tz', 'Asia/Seoul'),
        ('tzinput', None),  # this should be none (utc) since we are already putting datetimes converted to utc
        ('calendar', None),
    )

    _store = KiwoomOpenApiStore

    _ST_FROM, _ST_START, _ST_LIVE, _ST_HISTORBACK, _ST_OVER = range(5)

    def __init__(self, *args, **kwargs):
        self.k = self._store(*args, **kwargs)

        if self.p.dataname not in self.k.datanames:
            self.k.datanames.append(self.p.dataname)

        self.qlive = queue.Queue()
        self.qhist = queue.Queue()

        self.contractdetails = None

        self._statelivereconn = False
        self._storedmsg = dict()
        self._state = self._ST_OVER
        self._reconns = 0

        self._tz = self._gettz()

    def _timeoffset(self):
        return self.k.timeoffset()

    def isnaive(self, dt):
        return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None

    def asutc(self, dt, tz=None, naive=True):
        if tz is None:
            tz = self._tz
        if self.isnaive(dt) and tz is not None:
            dt = tz.localize(dt)
        dt = dt.astimezone(utc)
        if naive:
            dt = dt.replace(tzinfo=None)
        return dt

    def date2num(self, dt, tz=None): # pylint: disable=arguments-differ
        dt = self.asutc(dt, tz)
        return date2num(dt)

    def num2date(self, dt=None, tz=None, naive=False):
        if dt is None:
            dt = self.lines.datetime[0]
        if tz is None:
            tz = self._tz
        return num2date(dt, tz, naive)

    def fromtimestamp(self, timestamp, tz=None):
        if tz is None:
            tz = self._tz
        return datetime.datetime.fromtimestamp(timestamp, tz=tz)

    def islive(self):
        return not self.p.historical

    def setenvironment(self, env):
        super().setenvironment(env)
        env.addstore(self.k)

    def start(self):
        super().start()

        self.qlive = queue.Queue()
        self.qhist = queue.Queue()

        self._statelivereconn = False
        self._storedmsg = dict()
        self._state = self._ST_OVER

        self.k.start(data=self)

        otf = self.k.get_granularity(self.p.timeframe, self.p.compression)

        if otf is None:
            logging.warning('Given timeframe and compression not supported: (%s, %s)', self.p.timeframe, self.p.compression)
            self.put_notification(self.NOTSUPPORTED_TF)
            self._state = self._ST_OVER
            return

        self.contractdetails = cd = self.k.get_instrument(self.p.dataname)

        if cd is None:
            logging.warning('Given dataname is not supported')
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

        self._reconns = 0

    def _st_start(self, instart=True, tmout=None):
        if self.p.historical:
            self.put_notification(self.DELAYED)

            dtend = None
            if self.todate < float('inf'):
                dtend = self.num2date(self.todate)

            dtbegin = None
            if self.fromdate > float('-inf'):
                dtbegin = self.num2date(self.fromdate)

            self.qhist = self.k.candles(
                self.p.dataname, dtbegin, dtend,
                self.p.timeframe, self.p.compression)

            self._state = self._ST_HISTORBACK

            return True
        else:
            self.qlive = self.k.streaming_prices(self.p.dataname, tmout=tmout)

            if instart:
                self._statelivereconn = self.p.backfill_start
            else:
                self._statelivereconn = self.p.backfill

            if self._statelivereconn:
                self.put_notification(self.DELAYED)

            self._state = self._ST_LIVE

            if instart:
                self._reconns = self.p.reconnections

            if instart and not self.p.backfill_start:
                self.put_notification(self.DELAYED)

                msg = self.k.initial_today_historical_msg(data=self)

                self.qhist.put(msg)
                self.qhist.put({})

                self._state = self._ST_HISTORBACK

            return True

    def stop(self):
        super().stop()
        self.k.stop()

    def haslivedata(self):
        return bool(self._storedmsg or not self.qlive.empty())

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
                    self._st_start(instart=False, tmout=self.p.reconntimeout)
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
                    self._st_start(instart=False, tmout=self.p.reconntimeout)
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
                    dtbegin = self.num2date(self.fromdate)
                else:
                    dtbegin = None

                dtend = self.fromtimestamp(int(msg['time']) / 10 ** 6)

                self.qhist = self.k.candles(
                    self.p.dataname, dtbegin, dtend,
                    self.p.timeframe, self.p.compression)

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
        dtobj = self.fromtimestamp(int(msg['time']) / 10 ** 6)
        dt = self.date2num(dtobj)
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
        dtobj = self.fromtimestamp(int(msg['time']) / 10 ** 6)
        dt = self.date2num(dtobj)
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
