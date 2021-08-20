import atexit
import threading
import time

from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceMessageUtils import (
    convert_arguments_from_protobuf_to_python,
)
from koapy.backend.kiwoom_open_api_plus.utils.queue.QueueBasedIterableObserver import (
    QueueBasedIterableObserver,
)


class KiwoomOpenApiPlusServiceClientSideSignalConnector:
    def __init__(self, stub, name, executor):
        self._stub = stub
        self._name = name
        self._executor = executor
        self._lock = threading.RLock()
        self._observers = {}

        atexit.register(self.shutdown)

    def __del__(self):
        atexit.unregister(self.shutdown)

    def _stop_observer(self, observer):
        request = KiwoomOpenApiPlusService_pb2.BidirectionalListenRequest()
        request.stop_listen_request.time = time.time()
        observer.on_next(request)
        observer.on_completed()

    def _get_observer(self, callback, default=None):
        return self._observers.setdefault(self._name, {}).get(callback, default)

    def _remove_observer(self, callback):
        with self._lock:
            observer = self._get_observer(callback)
            if observer:
                self._stop_observer(observer)
                del self._observers[self._name][callback]
            return observer

    def _add_observer(self, callback):
        with self._lock:
            self._remove_observer(callback)
            observer = QueueBasedIterableObserver()
            self._observers[self._name][callback] = observer
            return observer

    def shutdown(self):
        with self._lock:
            for _name, observers in self._observers.items():
                for _callback, observer in observers.items():
                    self._stop_observer(observer)

    def connect(self, callback):
        with self._lock:
            observer = self._add_observer(callback)

            def fn():
                request = KiwoomOpenApiPlusService_pb2.BidirectionalListenRequest()
                request.listen_request.slots.append(self._name)
                observer.on_next(request)
                observer_iterator = iter(observer)
                response_iterator = self._stub.BidirectionalListen(observer_iterator)
                for response in response_iterator:
                    args = convert_arguments_from_protobuf_to_python(response.arguments)
                    callback(*args)
                    request = KiwoomOpenApiPlusService_pb2.BidirectionalListenRequest()
                    request.handled_request.time = time.time()
                    observer.on_next(request)

            future = self._executor.submit(fn)
            """
            def done(future):
                err = future.exception()
                if err:
                    raise err

            future.add_done_callback(done)
            """

    def disconnect(self, callback):
        with self._lock:
            self._remove_observer(callback)
