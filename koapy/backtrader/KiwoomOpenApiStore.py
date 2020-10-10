# pylint: disable=no-member

import time
import datetime
import threading
import collections

import pendulum
import backtrader as bt

from backtrader import TimeFrame
from backtrader.metabase import MetaParams
from backtrader.utils.py3 import queue, with_metaclass

from koapy.context.KiwoomOpenApiContext import KiwoomOpenApiContext
from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError
from koapy.backtrader.KiwoomOpenApiEventStreamer import KiwoomOpenApiEventStreamer

class KiwoomOpenApiJsonError(KiwoomOpenApiError):

    def __init__(self, code, message=None):
        if isinstance(code, KiwoomOpenApiError):
            err = code
            code = err.code
            message = err.message
        super().__init__(code, message)

    @property
    def error_response(self, description=None):
        response = {
            'code': self.code,
            'message': self.message,
            'description': description or '',
        }
        return response

class KiwoomOpenApiTimeFrameError(KiwoomOpenApiJsonError):

    def __init__(self):
        super().__init__(code=597, message='Not supported TimeFrame')

class HistoricalPriceRecord(collections.namedtuple('HistoricalPriceRecord', ['time', 'open', 'high', 'low', 'close', 'volume'])):

    __slots__ = ()

    @classmethod
    def from_tuple(cls, tup):
        if '일자' in tup._fields:
            time = pendulum.from_format(tup.일자, 'YYYYMMDD', tz='Asia/Seoul').timestamp() * (10 ** 6) # pylint: disable=redefined-outer-name
        elif '체결시간' in tup._fields:
            time = pendulum.from_format(tup.체결시간, 'YYYYMMDDhhmmss', tz='Asia/Seoul').timestamp() * (10 ** 6)
        else:
            raise KiwoomOpenApiError('Cannot specify time')
        open = abs(float(tup.시가)) # pylint: disable=redefined-builtin
        high = abs(float(tup.고가))
        low = abs(float(tup.저가))
        close = abs(float(tup.현재가))
        volume = abs(float(tup.거래량))
        return cls(time, open, high, low, close, volume)

    @classmethod
    def records_from_dataframe(cls, df):
        return [cls.from_tuple(tup) for tup in df[::-1].itertuples()]

    @classmethod
    def dict_records_from_dataframe(cls, df):
        return [msg._asdict() for msg in cls.records_from_dataframe(df)]

class API:

    # 우선은 최대한 기존 Oanda 구현을 유지한채로 맞춰서 동작할 수 있도록 구현해놓고
    # 추후 동작이 되는게 확인되면 천천히 하단 API 에 맞게 최적화를 하는 방향으로 작업하는 것으로...

    def __init__(self, context):
        self._context = context

    def __getattr__(self, name):
        return getattr(self._context, name)

    def get_instruments(self, account, instruments): # TODO: 계좌에 따라 시장이 다를 수 있음
        instruments = self.GetStockInfoAsDataFrame(instruments)
        instruments = [tup._asdict() for tup in instruments.itertuples(index=False)]
        response = {'instruments': instruments}
        return response

    def get_history(self, trcode, inputs, dtbegin=None, dtend=None):
        if trcode == 'opt10079':
            code = inputs['종목코드']
            interval = inputs['틱범위']
            adjusted_price = inputs.get('수정주가구분') == '1'
            df = self.GetTickStockDataAsDataFrame(code, interval, dtend, dtbegin, adjusted_price=adjusted_price)
        elif trcode == 'opt10080':
            code = inputs['종목코드']
            interval = inputs['틱범위']
            adjusted_price = inputs.get('수정주가구분') == '1'
            df = self.GetMinuteStockDataAsDataFrame(code, interval, dtend, dtbegin, adjusted_price=adjusted_price)
        elif trcode == 'opt10081':
            code = inputs['종목코드']
            adjusted_price = inputs.get('수정주가구분') == '1'
            df = self.GetDailyStockDataAsDataFrame(code, dtend, dtbegin, adjusted_price=adjusted_price)
        elif trcode == 'opt10082':
            code = inputs['종목코드']
            adjusted_price = inputs.get('수정주가구분') == '1'
            df = self.GetWeeklyStockDataAsDataFrame(code, dtend, dtbegin, adjusted_price=adjusted_price)
        elif trcode == 'opt10083':
            code = inputs['종목코드']
            adjusted_price = inputs.get('수정주가구분') == '1'
            df = self.GetMonthlyStockDataAsDataFrame(code, dtend, dtbegin, adjusted_price=adjusted_price)
        elif trcode == 'opt10094':
            code = inputs['종목코드']
            adjusted_price = inputs.get('수정주가구분') == '1'
            df = self.GetYearlyStockDataAsDataFrame(code, dtend, dtbegin, adjusted_price=adjusted_price)
        else:
            raise KiwoomOpenApiError('Unexpected trcode %s' % trcode)

        candles = HistoricalPriceRecord.dict_records_from_dataframe(df)
        response = {'candles': candles}
        return response

    def get_positions(self, account):
        _summary, foreach = self.GetAccountEvaluationStatusAsSeriesAndDataFrame(account)
        positions = [{
            'instrument': tup.종목코드,
            'side': 'buy',
            'units': float(tup.보유수량),
            'avgPrice': float(tup.매입금액) / float(tup.보유수량),
        } for tup in foreach.itertuples()]
        response = {'positions': positions}
        return response

    def get_account(self, account):
        deposit = self.GetDepositInfo(account)
        summary, _foreach = self.GetAccountEvaluationStatusAsSeriesAndDataFrame(account)
        response = {
            'marginAvail': float(deposit['주문가능금액']),
            'balance': float(summary['유가잔고평가액']),
        }
        return response

    def create_order(self, account, **kwargs):
        # TODO: Implement
        raise NotImplementedError
        response = {}
        return response

    def close_order(self, account, oid):
        # TODO: Implement
        raise NotImplementedError
        response = {}
        return response

class MetaSingleton(MetaParams):

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls._singleton = None

    def __call__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super().__call__(*args, **kwargs)

        return cls._singleton

class KiwoomOpenApiStore(with_metaclass(MetaSingleton, object)):

    BrokerCls = None  # broker class will auto register
    DataCls = None  # data class will auto register

    params = (
        ('account', ''),
        ('account_tmout', 10.0),
    )

    @classmethod
    def getdata(cls, *args, **kwargs):
        if cls.DataCls is None:
            from koapy.backtrader.KiwoomOpenApiData import KiwoomOpenApiData
            cls.DataCls = KiwoomOpenApiData
        return cls.DataCls(*args, **kwargs) # pylint: disable=not-callable

    @classmethod
    def getbroker(cls, *args, **kwargs):
        if cls.BrokerCls is None:
            from koapy.backtrader.KiwoomOpenApiBroker import KiwoomOpenApiBroker
            cls.BrokerCls = KiwoomOpenApiBroker
        return cls.BrokerCls(*args, **kwargs) # pylint: disable=not-callable

    def __init__(self, context=None):
        super().__init__()

        self.notifs = collections.deque()

        self._env = None
        self.broker = None
        self.datas = list()

        if context is None:
            context = KiwoomOpenApiContext()

        self._context = context
        self._context.EnsureConnected()

        self.context = API(self._context)

        self._cash = 0.0
        self._value = 0.0
        self._evt_acct = threading.Event()

        self.q_account = None
        self.q_ordercreate = None
        self.q_orderclose = None

    def start(self, data=None, broker=None):
        if data is None and broker is None:
            return

        if data is not None:
            self._env = data._env # pylint: disable=protected-access
            self.datas.append(data)

            if self.broker is not None:
                self.broker.data_started(data)

        elif broker is not None:
            self.broker = broker
            self.streaming_events()
            self.broker_threads()

    def stop(self):
        pass

    def put_notification(self, msg, *args, **kwargs):
        self.notifs.append((msg, args, kwargs))

    def get_notifications(self):
        self.notifs.append(None)
        return [x for x in iter(self.notifs.popleft, None)]

    _GRANULARITIES = {
        (TimeFrame.Ticks, 1):    ('opt10079', {'종목코드': '', '틱범위': '1', '수정주가구분': '1'}),
        (TimeFrame.Ticks, 3):    ('opt10079', {'종목코드': '', '틱범위': '3', '수정주가구분': '1'}),
        (TimeFrame.Ticks, 5):    ('opt10079', {'종목코드': '', '틱범위': '5', '수정주가구분': '1'}),
        (TimeFrame.Ticks, 10):   ('opt10079', {'종목코드': '', '틱범위': '10', '수정주가구분': '1'}),
        (TimeFrame.Ticks, 30):   ('opt10079', {'종목코드': '', '틱범위': '30', '수정주가구분': '1'}),
        (TimeFrame.Minutes, 1):  ('opt10080', {'종목코드': '', '틱범위': '1', '수정주가구분': '1'}),
        (TimeFrame.Minutes, 3):  ('opt10080', {'종목코드': '', '틱범위': '3', '수정주가구분': '1'}),
        (TimeFrame.Minutes, 5):  ('opt10080', {'종목코드': '', '틱범위': '5', '수정주가구분': '1'}),
        (TimeFrame.Minutes, 10): ('opt10080', {'종목코드': '', '틱범위': '10', '수정주가구분': '1'}),
        (TimeFrame.Minutes, 15): ('opt10080', {'종목코드': '', '틱범위': '15', '수정주가구분': '1'}),
        (TimeFrame.Minutes, 30): ('opt10080', {'종목코드': '', '틱범위': '30', '수정주가구분': '1'}),
        (TimeFrame.Minutes, 45): ('opt10080', {'종목코드': '', '틱범위': '45', '수정주가구분': '1'}),
        (TimeFrame.Minutes, 60): ('opt10080', {'종목코드': '', '틱범위': '60', '수정주가구분': '1'}),
        (TimeFrame.Days, 1):     ('opt10081', {'종목코드': '', '기준일자': '', '수정주가구분': '1'}),
        (TimeFrame.Weeks, 1):    ('opt10082', {'종목코드': '', '기준일자': '', '끝일자': '', '수정주가구분': '1'}),
        (TimeFrame.Months, 1):   ('opt10083', {'종목코드': '', '기준일자': '', '끝일자': '', '수정주가구분': '1'}),
        (TimeFrame.Years, 1):    ('opt10094', {'종목코드': '', '기준일자': '', '끝일자': '', '수정주가구분': '1'}),
    }

    def get_granularity(self, timeframe, compression, default=None):
        return self._GRANULARITIES.get((timeframe, compression), default)

    def get_instrument(self, dataname):
        try:
            insts = self.context.get_instruments(self.p.account, instruments=dataname)
        except KiwoomOpenApiError:
            return None

        i = insts.get('instruments', [{}])
        return i[0] or None

    def streaming_events(self, tmout=None):
        q = queue.Queue()
        kwargs = {'q': q, 'tmout': tmout}

        t = threading.Thread(target=self._t_streaming_listener, kwargs=kwargs)
        t.daemon = True
        t.start()

        t = threading.Thread(target=self._t_streaming_events, kwargs=kwargs)
        t.daemon = True
        t.start()
        return q

    def _t_streaming_listener(self, q, tmout=None):
        while True:
            trans = q.get()
            self._transaction(trans)

    def _t_streaming_events(self, q, tmout=None):
        if tmout is not None:
            time.sleep(tmout)
        streamer = KiwoomOpenApiEventStreamer(self.context, q)
        streamer.events()

    def candles(self, dataname, dtbegin, dtend, timeframe, compression): # pylint: disable=unused-argument
        kwargs = locals().copy()
        kwargs.pop('self')
        kwargs['q'] = q = queue.Queue()
        t = threading.Thread(target=self._t_candles, kwargs=kwargs)
        t.daemon = True
        t.start()
        return q

    def _t_candles(self, dataname, dtbegin, dtend, timeframe, compression, q):
        trcode, inputs = self.get_granularity(timeframe, compression, (None, None))

        if trcode is None:
            e = KiwoomOpenApiTimeFrameError()
            q.put(e.error_response)
            return

        inputs = inputs.copy()
        inputs['종목코드'] = dataname

        if dtbegin is not None:
            if '끝일자' in inputs:
                inputs['끝일자'] = dtbegin.strftime('%Y%m%d')

        if dtend is not None:
            if '기준일자' in inputs:
                inputs['기준일자'] = dtend.strftime('%Y%m%d')

        try:
            response = self.context.get_history(trcode, inputs, dtbegin, dtend)
        except KiwoomOpenApiError as e:
            q.put(KiwoomOpenApiJsonError(e).error_response)
            q.put(None)
            return

        for candle in response.get('candles', []):
            q.put(candle)

        q.put({})

    def streaming_prices(self, dataname, tmout=None):
        q = queue.Queue()
        kwargs = {'q': q, 'dataname': dataname, 'tmout': tmout}
        t = threading.Thread(target=self._t_streaming_prices, kwargs=kwargs)
        t.daemon = True
        t.start()
        return q

    def _t_streaming_prices(self, dataname, q, tmout):
        if tmout is not None:
            time.sleep(tmout)
        streamer = KiwoomOpenApiEventStreamer(self.context, q)
        streamer.rates(dataname)

    def get_cash(self):
        return self._cash

    def get_value(self):
        return self._value

    def get_positions(self):
        try:
            positions = self.context.get_positions(self.p.account)
        except KiwoomOpenApiError:
            return None

        poslist = positions.get('positions', [])
        return poslist


    def broker_threads(self):
        self.q_account = queue.Queue()
        self.q_account.put(True)  # force an immediate update
        t = threading.Thread(target=self._t_account)
        t.daemon = True
        t.start()

        self.q_ordercreate = queue.Queue()
        t = threading.Thread(target=self._t_order_create)
        t.daemon = True
        t.start()

        self.q_orderclose = queue.Queue()
        t = threading.Thread(target=self._t_order_cancel)
        t.daemon = True
        t.start()

        # Wait once for the values to be set
        self._evt_acct.wait(self.p.account_tmout)

    def _t_account(self):
        while True:
            try:
                msg = self.q_account.get(timeout=self.p.account_tmout)
                if msg is None:
                    break  # end of thread
            except queue.Empty:  # tmout -> time to refresh
                pass

            try:
                accinfo = self.context.get_account(self.p.account)
            except Exception as e: # pylint: disable=broad-except
                self.put_notification(e)
                continue

            try:
                self._cash = accinfo['marginAvail']
                self._value = accinfo['balance']
            except KeyError:
                pass

            self._evt_acct.set()


    # from below, it's related to processing orders


    _ORDEREXECS = {
        bt.Order.Market: 'market',
        bt.Order.Limit: 'limit',
        bt.Order.Stop: 'stop',
        bt.Order.StopLimit: 'stop',
    }

    def order_create(self, order, stopside=None, takeside=None, **kwargs):
        okwargs = dict()
        okwargs['instrument'] = order.data._dataname
        okwargs['units'] = abs(order.created.size)
        okwargs['side'] = 'buy' if order.isbuy() else 'sell'
        okwargs['type'] = self._ORDEREXECS[order.exectype]
        if order.exectype != bt.Order.Market:
            okwargs['price'] = order.created.price
            if order.valid is None:
                # 1 year and datetime.max fail ... 1 month works
                valid = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            else:
                valid = order.data.num2date(order.valid)
                # To timestamp with seconds precision
            okwargs['expiry'] = int((valid - self._DTEPOCH).total_seconds())

        if order.exectype == bt.Order.StopLimit:
            okwargs['lowerBound'] = order.created.pricelimit
            okwargs['upperBound'] = order.created.pricelimit

        if order.exectype == bt.Order.StopTrail:
            okwargs['trailingStop'] = order.trailamount

        if stopside is not None:
            okwargs['stopLoss'] = stopside.price

        if takeside is not None:
            okwargs['takeProfit'] = takeside.price

        okwargs.update(**kwargs)  # anything from the user

        self.q_ordercreate.put((order.ref, okwargs,))
        return order

    _OIDSINGLE = ['orderOpened', 'tradeOpened', 'tradeReduced']
    _OIDMULTIPLE = ['tradesClosed']

    def _t_order_create(self):
        while True:
            msg = self.q_ordercreate.get()
            if msg is None:
                break

            oref, okwargs = msg
            try:
                o = self.context.create_order(self.p.account, **okwargs)
            except Exception as e:
                self.put_notification(e)
                self.broker._reject(oref)
                return

            # Ids are delivered in different fields and all must be fetched to
            # match them (as executions) to the order generated here
            oids = list()
            for oidfield in self._OIDSINGLE:
                if oidfield in o and 'id' in o[oidfield]:
                    oids.append(o[oidfield]['id'])

            for oidfield in self._OIDMULTIPLE:
                if oidfield in o:
                    for suboidfield in o[oidfield]:
                        oids.append(suboidfield['id'])

            if not oids:
                self.broker._reject(oref)
                return

            self._orders[oref] = oids[0]
            self.broker._submit(oref)
            if okwargs['type'] == 'market':
                self.broker._accept(oref)  # taken immediately

            for oid in oids:
                self._ordersrev[oid] = oref  # maps ids to backtrader order

                # An transaction may have happened and was stored
                tpending = self._transpend[oid]
                tpending.append(None)  # eom marker
                while True:
                    trans = tpending.popleft()
                    if trans is None:
                        break
                    self._process_transaction(oid, trans)

    def order_cancel(self, order):
        self.q_orderclose.put(order.ref)
        return order

    def _t_order_cancel(self):
        while True:
            oref = self.q_orderclose.get()
            if oref is None:
                break

            oid = self._orders.get(oref, None)
            if oid is None:
                continue  # the order is no longer there
            try:
                o = self.context.close_order(self.p.account, oid)
            except Exception as e:
                continue  # not cancelled - FIXME: notify

            self.broker._cancel(oref)

    _X_ORDER_CREATE = ('STOP_ORDER_CREATE',
                       'LIMIT_ORDER_CREATE', 'MARKET_IF_TOUCHED_ORDER_CREATE',)

    def _transaction(self, trans):
        # Invoked from Streaming Events. May actually receive an event for an
        # oid which has not yet been returned after creating an order. Hence
        # store if not yet seen, else forward to processer
        ttype = trans['type']
        if ttype == 'MARKET_ORDER_CREATE':
            try:
                oid = trans['tradeReduced']['id']
            except KeyError:
                try:
                    oid = trans['tradeOpened']['id']
                except KeyError:
                    return  # cannot do anything else

        elif ttype in self._X_ORDER_CREATE:
            oid = trans['id']
        elif ttype == 'ORDER_FILLED':
            oid = trans['orderId']

        elif ttype == 'ORDER_CANCEL':
            oid = trans['orderId']

        elif ttype == 'TRADE_CLOSE':
            oid = trans['id']
            pid = trans['tradeId']
            if pid in self._orders and False:  # Know nothing about trade
                return  # can do nothing

            # Skip above - at the moment do nothing
            # Received directly from an event in the WebGUI for example which
            # closes an existing position related to order with id -> pid
            # COULD BE DONE: Generate a fake counter order to gracefully
            # close the existing position
            msg = ('Received TRADE_CLOSE for unknown order, possibly generated'
                   ' over a different client or GUI')
            self.put_notification(msg, trans)
            return

        else:  # Go aways gracefully
            try:
                oid = trans['id']
            except KeyError:
                oid = 'None'

            msg = 'Received {} with oid {}. Unknown situation'
            msg = msg.format(ttype, oid)
            self.put_notification(msg, trans)
            return

        try:
            oref = self._ordersrev[oid]
            self._process_transaction(oid, trans)
        except KeyError:  # not yet seen, keep as pending
            self._transpend[oid].append(trans)

    _X_ORDER_FILLED = ('MARKET_ORDER_CREATE',
                       'ORDER_FILLED', 'TAKE_PROFIT_FILLED',
                       'STOP_LOSS_FILLED', 'TRAILING_STOP_FILLED',)

    def _process_transaction(self, oid, trans):
        try:
            oref = self._ordersrev.pop(oid)
        except KeyError:
            return

        ttype = trans['type']

        if ttype in self._X_ORDER_FILLED:
            size = trans['units']
            if trans['side'] == 'sell':
                size = -size
            price = trans['price']
            self.broker._fill(oref, size, price, ttype=ttype)

        elif ttype in self._X_ORDER_CREATE:
            self.broker._accept(oref)
            self._ordersrev[oid] = oref

        elif ttype in 'ORDER_CANCEL':
            reason = trans['reason']
            if reason == 'ORDER_FILLED':
                pass  # individual execs have done the job
            elif reason == 'TIME_IN_FORCE_EXPIRED':
                self.broker._expire(oref)
            elif reason == 'CLIENT_REQUEST':
                self.broker._cancel(oref)
            else:  # default action ... if nothing else
                self.broker._reject(oref)
