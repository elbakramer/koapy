import atexit
import threading

from concurrent import futures

from koapy.grpc import KiwoomOpenApiService_pb2
from koapy.grpc.observer.QueueBasedIterableObserver import QueueBasedIterableObserver

from koapy.grpc.KiwoomOpenApiService import convert_arguments_from_protobuf_to_python

from koapy.config import config

class KiwoomOpenApiServiceClientSideSignalConnector:

    _lock = threading.RLock()
    _observers = {}
    _max_workers = config.get_int('koapy.grpc.client.signal_connector.max_workers', 8)
    _executor = futures.ThreadPoolExecutor(max_workers=_max_workers)

    def __init__(self, stub, name):
        self._stub = stub
        self._name = name

    @classmethod
    def _stop_observer(cls, observer):
        request = KiwoomOpenApiService_pb2.BidirectionalListenRequest()
        request.stop_listen_request.id = '' # pylint: disable=no-member,pointless-statement
        observer.on_next(request)
        observer.on_completed()

    def _get_observer(self, callback, default=None):
        return self._observers.setdefault(self._stub, {}).setdefault(self._name, {}).get(callback, default)

    def _remove_observer(self, callback):
        with self._lock:
            observer = self._get_observer(callback)
            if observer:
                self._stop_observer(observer)
                del self._observers[self._stub][self._name][callback]
            return observer

    def _add_observer(self, callback):
        with self._lock:
            self._remove_observer(callback)
            observer = QueueBasedIterableObserver()
            self._observers[self._stub][self._name][callback] = observer
            return observer

    @classmethod
    def shutdown(cls):
        with cls._lock:
            for _stub, names in cls._observers.items():
                for _name, observers in names.items():
                    for _callback, observer in observers.items():
                        cls._stop_observer(observer)
        cls._executor.shutdown(False)

    def connect(self, callback):
        with self._lock:
            observer = self._add_observer(callback)
            def fn():
                request = KiwoomOpenApiService_pb2.BidirectionalListenRequest()
                request.listen_request.slots.append(self._name) # pylint: disable=no-member
                observer.on_next(request)
                observer_iterator = iter(observer)
                for i, response in enumerate(self._stub.BidirectionalListen(observer_iterator)):
                    args = convert_arguments_from_protobuf_to_python(response.arguments)
                    callback(*args)
                    request = KiwoomOpenApiService_pb2.BidirectionalListenRequest()
                    request.handled_request.id = i # pylint: disable=no-member,pointless-statement
                    observer.on_next(request)
            future = self._executor.submit(fn)
            def done(future):
                err = future.exception()
                if err:
                    raise err
            future.add_done_callback(done)

    def disconnect(self, callback):
        with self._lock:
            self._remove_observer(callback)

atexit.register(KiwoomOpenApiServiceClientSideSignalConnector.shutdown)
