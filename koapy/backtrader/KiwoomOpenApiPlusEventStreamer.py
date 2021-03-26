import datetime
import logging
import threading

import rx

from rx import operators as ops
from rx.subject import Subject
from rx.scheduler import ThreadPoolScheduler
from rx.core.typing import Observer

from exchange_calendars import get_calendar

from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver import QueueBasedIterableObserver
from koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedBufferedIterator import QueueBasedBufferedIterator
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import KiwoomOpenApiPlusRealType

from koapy.utils.logging.Logging import Logging

class KiwoomOpenApiPlusPriceEventChannel(Logging):

    _krx_timezone = get_calendar('XKRX').tz

    def __init__(self, stub):
        self._stub = stub
        self._fid_list = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name('주식시세')

        self._request_observer = QueueBasedIterableObserver()
        self._request_iterator = iter(self._request_observer)
        self._response_iterator = self._stub.BidirectionalRealCall(self._request_iterator)
        self._response_subject = Subject()
        self._response_scheduler_max_workers = 8
        self._response_scheduler = ThreadPoolScheduler(self._response_scheduler_max_workers)
        self._buffered_response_iterator = QueueBasedBufferedIterator(self._response_iterator)
        self._response_observable = rx.from_iterable(self._buffered_response_iterator, self._response_scheduler)
        self._response_subscription = self._response_observable.subscribe(self._response_subject)

        self._subjects_by_code = {}

        self.initialize()

    def close(self):
        for _code, (_subject, subscription) in self._subjects_by_code.items():
            subscription.dispose()
        self._response_subscription.dispose()
        self._buffered_response_iterator.stop()
        self._response_iterator.cancel()

    def __del__(self):
        self.close()

    def initialize(self):
        request = KiwoomOpenApiPlusService_pb2.BidirectionalRealRequest()
        request.initialize_request.fid_list.extend(self._fid_list) # pylint: disable=no-member
        self._request_observer.on_next(request)

    def register_code(self, code):
        request = KiwoomOpenApiPlusService_pb2.BidirectionalRealRequest()
        code_list = [code]
        fid_list = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name('주식시세')
        request.register_request.code_list.extend(code_list) # pylint: disable=no-member
        request.register_request.fid_list.extend(fid_list) # pylint: disable=no-member
        self._request_observer.on_next(request)
        self.logger.debug('Registering code %s for real events', code)

    def is_for_code(self, response, code):
        return response.arguments[0].string_value == code

    def filter_for_code(self, code):
        return ops.filter(lambda response: self.is_for_code(response, code))

    def is_valid_price_event(self, response):
        return all(name in response.single_data.names for name in ['20', '27', '28'])

    def filter_price_event(self):
        return ops.filter(self.is_valid_price_event)

    def time_to_timestamp(self, fid20):
        dt = datetime.datetime.now(self._krx_timezone).date()
        tm = datetime.datetime.strptime(fid20, '%H%M%S').time()
        dt = datetime.datetime.combine(dt, tm)
        dt = self._krx_timezone.localize(dt)
        return dt.timestamp() * (10 ** 6)

    def event_to_dict(self, response):
        single_data = dict(zip(response.single_data.names, response.single_data.values))
        result = {
            'time': self.time_to_timestamp(single_data['20']),
            'bid': abs(float(single_data['28'])),
            'ask': abs(float(single_data['27'])),
        }
        return result

    def convert_to_dict(self):
        return ops.map(self.event_to_dict)

    def get_observable_for_code(self, code):
        self.register_code(code)
        if code not in self._subjects_by_code:
            subject = Subject()
            subscription = self._response_subject.pipe(
                self.filter_for_code(code),
                self.filter_price_event(),
                self.convert_to_dict(),
            ).subscribe(subject)
            self._subjects_by_code[code] = (subject, subscription)
        subject, subscription = self._subjects_by_code[code]
        return subject

class KiwoomOpenApiPlusOrderEventChannel:

    def __init__(self, stub):
        self._stub = stub

        request = KiwoomOpenApiPlusService_pb2.ListenRequest()
        self._response_iterator = self._stub.OrderListen(request)
        self._response_subject = Subject()
        self._response_scheduler_max_workers = 8
        self._response_scheduler = ThreadPoolScheduler(self._response_scheduler_max_workers)
        self._buffered_response_iterator = QueueBasedBufferedIterator(self._response_iterator)
        self._response_observable = rx.from_iterable(self._buffered_response_iterator, self._response_scheduler)
        self._response_subscription = self._response_observable.subscribe(self._response_subject)

        self._observable = Subject()
        self._subscription = self._response_subject.pipe(
            self.filter_chejan_response(),
            self.convert_to_dict(),
        ).subscribe(self._observable)

    def close(self):
        self._subscription.dispose()
        self._response_subscription.dispose()
        self._buffered_response_iterator.stop()
        self._response_iterator.cancel()

    def __del__(self):
        self.close()

    def is_chejan_response(self, response):
        name = response.name
        gubun = response.arguments[0].string_value
        if name == 'OnReceiveChejanData' and gubun == '0':
            data = dict(zip(response.single_data.names, response.single_data.values))
            order_type = data['주문구분']
            hoga_type = data['매매구분']
            status = data['주문상태']
            market_order_created_and_filled = order_type in ['+매수', '-매도'] and hoga_type in ['시장가'] and status in ['체결']
            limit_order_created = order_type in ['+매수', '-매도'] and hoga_type in ['보통'] and status in ['접수'] and data['819'] in ['0'] # 취소 확인 뒤에 오는 원주문 이벤트는 819 가 1 로 들어오는 것 같음
            order_filled = order_type in ['+매수', '-매도'] and status in ['체결']
            order_canceled = order_type in ['매수취소', '매도취소'] and status in ['확인']
            condition = any([
                market_order_created_and_filled,
                limit_order_created,
                order_filled,
                order_canceled,
            ])
            return condition
        return False

    def filter_chejan_response(self):
        return ops.filter(self.is_chejan_response)

    def event_to_dict(self, response):
        result = {}
        data = dict(zip(response.single_data.names, response.single_data.values))
        original_order_no = data['원주문번호']
        if int(original_order_no):
            status = data['주문상태']
            if status == '확인':
                reject_reason = data['거부사유']
                result = {
                    'type': 'ORDER_CANCEL',
                    'orderId': original_order_no,
                    'reason': reject_reason if int(reject_reason) else 'ORDER_FILLED',
                }
        else:
            status = data['주문상태']
            hoga_type = data['매매구분']
            if status == '접수':
                if hoga_type == '보통':
                    order_no = data['주문번호']
                    result = {
                        'type': 'LIMIT_ORDER_CREATE',
                        'id': order_no,
                    }
                elif hoga_type == '시장가':
                    pass
                else:
                    self.logger.warning('Unexpected hoga type %s', hoga_type)
            elif status == '체결':
                if hoga_type == '보통':
                    order_no = data['주문번호']
                    units = data['단위체결량']
                    buy_or_sell = data['주문구분']
                    side = {
                        '+매수': 'buy',
                        '-매도': 'sell',
                    }[buy_or_sell]
                    price = data['단위체결가']
                    result = {
                        'type': 'ORDER_FILLED',
                        'orderId': order_no,
                        'units': int(units),
                        'side': side,
                        'price': abs(float(price)),
                    }
                elif hoga_type == '시장가':
                    order_no = data['주문번호']
                    units = data['단위체결량']
                    buy_or_sell = data['주문구분']
                    side = {
                        '+매수': 'buy',
                        '-매도': 'sell',
                    }[buy_or_sell]
                    price = data['단위체결가']
                    result = {
                        'type': 'MARKET_ORDER_CREATE',
                        'id': order_no,
                        'tradeOpened': {'id': order_no},
                        'units': int(units),
                        'side': side,
                        'price': abs(float(price)),
                    }
                else:
                    self.logger.warning('Unexpected hoga type %s', hoga_type)
            else:
                self.logger.warning('Unexcpected status %s', status)
        return result

    def convert_to_dict(self):
        return ops.map(self.event_to_dict)

    def get_observable(self):
        return self._observable

class KiwoomOpenApiPlusEventStreamer(Observer, Logging):

    _price_event_channels_by_stub = {}
    _order_event_channels_by_stub = {}

    _lock = threading.RLock()

    def __init__(self, stub, queue):
        super().__init__()
        self._stub = stub
        self._queue = queue

    def on_next(self, value):
        self._queue.put(value)

    def on_error(self, error):
        self.logger.error('Streamer.on_error(%s)', error)

    def on_completed(self):
        pass

    def rates(self, code):
        with self._lock:
            if self._stub not in self._price_event_channels_by_stub:
                self._price_event_channels_by_stub[self._stub] = KiwoomOpenApiPlusPriceEventChannel(self._stub)
            event_channel = self._price_event_channels_by_stub[self._stub]
        subscription = event_channel.get_observable_for_code(code).subscribe(self)
        self.logger.debug('Subscribing rates for code %s', code)
        return subscription

    def events(self):
        with self._lock:
            if self._stub not in self._order_event_channels_by_stub:
                self._order_event_channels_by_stub[self._stub] = KiwoomOpenApiPlusOrderEventChannel(self._stub)
            event_channel = self._order_event_channels_by_stub[self._stub]
        subscription = event_channel.get_observable().subscribe(self)
        self.logger.debug('Subscribing order events')
        return subscription
