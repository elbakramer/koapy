import logging

import rx
import pendulum

from rx import operators as ops
from rx.subject import Subject
from rx.scheduler import ThreadPoolScheduler
from rx.core.typing import Observer

from koapy.grpc import KiwoomOpenApiService_pb2
from koapy.grpc.utils.QueueBasedIterableObserver import QueueBasedIterableObserver
from koapy.grpc.utils.QueueBasedBufferedIterator import QueueBasedBufferedIterator

from koapy.openapi.RealType import RealType

class KiwoomOpenApiPriceEventChannel:

    def __init__(self, stub):
        self._stub = stub
        self._fid_list = []

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
        self._response_iterator.cancel()

    def __del__(self):
        self.close()

    def initialize(self):
        request = KiwoomOpenApiService_pb2.BidirectionalRealRequest()
        request.initialize_request.fid_list.extend(self._fid_list) # pylint: disable=no-member
        self._request_observer.on_next(request)

    def register_code(self, code):
        request = KiwoomOpenApiService_pb2.BidirectionalRealRequest()
        code_list = [code]
        fid_list = RealType.get_fids_by_realtype('주식시세')
        request.register_request.code_list.extend(code_list) # pylint: disable=no-member
        request.register_request.fid_list.extend(fid_list) # pylint: disable=no-member
        self._request_observer.on_next(request)
        logging.debug('Registering code %s for real events', code)

    def is_for_code(self, response, code):
        return response.arguments[0].string_value == code

    def filter_for_code(self, code):
        return ops.filter(lambda response: self.is_for_code(response, code))

    def is_valid_price_event(self, response):
        return all(name in response.single_output.names for name in ['27', '28'])

    def filter_price_event(self):
        return ops.filter(self.is_valid_price_event)

    def time_to_timestamp(self, fid20):
        if fid20 is None:
            dt = pendulum.now()
        else:
            dt = pendulum.now()
        return dt.timestamp() * (10 ** 6)

    def event_to_dict(self, response):
        single_output = dict(zip(response.single_output.names, response.single_output.values))
        result = {
            'time': self.time_to_timestamp(single_output.get('20')),
            'bid': single_output['28'],
            'ask': single_output['27'],
        }
        return result

    def convert_to_dict(self):
        return ops.map(self.event_to_dict)

    def get_observable_for_code(self, code):
        self.register_code(code)
        if code not in self._subjects_by_code:
            subject = Subject()
            self._response_subject.pipe(
                self.filter_for_code(code),
                self.filter_price_event(),
                self.convert_to_dict(),
            ).subscribe(subject)
            self._subjects_by_code[code] = subject
        subject = self._subjects_by_code[code]
        return subject

class KiwoomOpenApiOrderEventChannel:

    def __init__(self, stub):
        self._stub = stub
        self._slots = [
            'OnReceiveMsg',
            'OnReceiveTrData',
            'OnReceiveChejanData',
            'OnEventConnect',
        ]

        request = KiwoomOpenApiService_pb2.ListenRequest()
        request.slots.extend(self._slots) # pylint: disable=no-member
        self._response_iterator = self._stub.Listen(request)
        self._subscription = rx.from_iterable(self._response_iterator).subscribe(self)

    def close(self):
        self._subscription.dispose()
        self._response_iterator.cancel()

    def dispose(self):
        self.close()

    def __del__(self):
        self.close()

class KiwoomOpenApiEventStreamer(Observer):

    _price_event_channels_by_stub = {}

    def __init__(self, stub, queue):
        super().__init__()
        self._stub = stub
        self._queue = queue

    def on_next(self, value):
        self._queue.put(value)

    def on_error(self, error):
        logging.debug('Streamer.on_error %s', error)
        self._queue.put(error)

    def on_completed(self):
        pass

    def rates(self, code):
        if self._stub not in self._price_event_channels_by_stub:
            self._price_event_channels_by_stub[self._stub] = KiwoomOpenApiPriceEventChannel(self._stub)
        event_channel = self._price_event_channels_by_stub[self._stub]
        subscription = event_channel.get_observable_for_code(code).subscribe(self)
        logging.debug('Subscribing rates for code %s', code)
        return subscription

    def events(self):
        return NotImplemented
