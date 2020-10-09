# pylint: disable=no-member

import time
import threading
import collections

import pendulum

from backtrader import TimeFrame
from backtrader.metabase import MetaParams
from backtrader.utils.py3 import queue, with_metaclass

import koapy

from koapy.grpc.event.KiwoomOpenApiEventStreamer import KiwoomOpenApiEventStreamer

class KiwoomOpenApiJsonError(koapy.KiwoomOpenApiError):

    def __init__(self, code, message=None):
        if isinstance(code, koapy.KiwoomOpenApiError):
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

class Message(collections.namedtuple('Message', ['time', 'open', 'high', 'low', 'close', 'volume'])):

    __slots__ = ()

    @classmethod
    def from_tuple(cls, tup):
        if '일자' in tup._fields:
            time = pendulum.from_format(tup.일자, 'YYYYMMDD', tz='Asia/Seoul').timestamp() * (10 ** 6)
        elif '체결시간' in tup._fields:
            time = pendulum.from_format(tup.체결시간, 'YYYYMMDDhhmmss', tz='Asia/Seoul').timestamp() * (10 ** 6)
        else:
            raise koapy.KiwoomOpenApiError('Cannot specify time')
        open = abs(float(tup.시가)) # pylint: disable=redefined-builtin
        high = abs(float(tup.고가))
        low = abs(float(tup.저가))
        close = abs(float(tup.현재가))
        volume = abs(float(tup.거래량))
        return cls(time, open, high, low, close, volume)

    @classmethod
    def messages_from_dataframe(cls, df):
        return [cls.from_tuple(tup) for tup in df[::-1].itertuples()]

    @classmethod
    def dict_messages_from_dataframe(cls, df):
        return [msg._asdict() for msg in cls.messages_from_dataframe(df)]

class API(koapy.KiwoomOpenApiContext):

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
            raise koapy.KiwoomOpenApiError('Unexpected trcode %s' % trcode)

        candles = Message.dict_messages_from_dataframe(df)
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

class MetaSingleton(MetaParams):

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls._singleton = None

    def __call__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super().__call__(*args, **kwargs)

        return cls._singleton

class KiwoomOpenApiStore(with_metaclass(MetaSingleton, object)):

    BrokerCls = None  # broker class will autoregister
    DataCls = None  # data class will auto register

    params = (
        ('account', ''),
    )

    @classmethod
    def getdata(cls, *args, **kwargs):
        '''Returns ``DataCls`` with args, kwargs'''
        return cls.DataCls(*args, **kwargs) # pylint: disable=not-callable

    @classmethod
    def getbroker(cls, *args, **kwargs):
        '''Returns broker with *args, **kwargs from registered ``BrokerCls``'''
        return cls.BrokerCls(*args, **kwargs) # pylint: disable=not-callable

    def __init__(self):
        super().__init__()

        self.notifs = collections.deque()

        self._env = None
        self.broker = None
        self.datas = list()

        self.oapi = API()

        self._cash = 0.0
        self._value = 0.0
        self._evt_acct = threading.Event()

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
            insts = self.oapi.get_instruments(self.p.account, instruments=dataname)
        except koapy.KiwoomOpenApiError:
            return None

        i = insts.get('instruments', [{}])
        return i[0] or None

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
            response = self.oapi.get_history(trcode, inputs, dtbegin, dtend)
        except koapy.KiwoomOpenApiError as e:
            q.put(KiwoomOpenApiJsonError(e).error_response)
            q.put(None)
            return

        for candle in response.get('candles', []):
            q.put(candle)

        q.put({})

    def streaming_prices(self, dataname, timeout=None):
        q = queue.Queue()
        kwargs = {'q': q, 'dataname': dataname, 'timeout': timeout}
        t = threading.Thread(target=self._t_streaming_prices, kwargs=kwargs)
        t.daemon = True
        t.start()
        return q

    def _t_streaming_prices(self, dataname, q, timeout):
        if timeout is not None:
            time.sleep(timeout)
        streamer = KiwoomOpenApiEventStreamer(self.oapi, q)
        streamer.rates(dataname)

    def get_cash(self):
        return self._cash

    def get_value(self):
        return self._value

    def get_positions(self):
        try:
            positions = self.oapi.get_positions(self.p.account)
        except koapy.KiwoomOpenApiError:
            return None

        poslist = positions.get('positions', [])
        return poslist
