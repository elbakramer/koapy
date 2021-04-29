import queue
import threading

import pythoncom
import win32com.client

from koapy.backend.daishin_cybos_plus.proxy import (
    CybosPlusProxyService_pb2,
    CybosPlusProxyService_pb2_grpc,
)
from koapy.backend.daishin_cybos_plus.proxy.CybosPlusMessageUtils import (
    AssignPrimitive,
    ExtractPrimitive,
)


class CybosPlusEvent:
    def __init__(self, iterator):
        self._iterator = iterator
        self._done = threading.Event()

    def __del__(self):
        self.done()

    def done(self):
        self._done.set()
        self._iterator._events.task_done()

    def wait_for_done(self):
        self._done.wait()


class CybosPlusEventIterator:
    def __init__(self, handler):
        self._handler = handler
        self._events = queue.Queue()
        self._sentinel = object()
        self._invalid = False
        with self._handler._lock:
            self._handler._iterators.append(self)

    def __del__(self):
        self._invalid = True
        self._events.put(self._sentinel)
        with self._handler._lock:
            if self in self._handler._iterators:
                self._handler._iterators.remove(self)

    def notify(self):
        if not self._invalid:
            event = CybosPlusEvent(self)
            self._events.put(event)
            return event
        else:
            raise ValueError

    def __next__(self):
        if self._invalid:
            raise StopIteration
        event = self._events.get()
        if event is self._sentinel:
            raise StopIteration
        return event


class CybosPlusEventHandler:
    def __init__(self):
        self._lock = threading.RLock()
        self._iterators = []

    def OnRecieved(self):
        with self._lock:
            events = [iterator.notify() for iterator in self._iterators]
        for event in events:
            event.wait_for_done()

    def __iter__(self):
        return CybosPlusEventIterator(self)


class CybosPlusProxyServiceServicer(
    CybosPlusProxyService_pb2_grpc.CybosPlusProxyServiceServicer
):

    _lock = threading.RLock()

    _dispatches = {}
    _handlers = {}

    def _EnsureDispatch(self, prog):
        if prog not in self._dispatches:
            with self._lock:
                if prog not in self._dispatches:
                    pythoncom.CoInitialize()  # pylint: disable=no-member
                    dispatch = win32com.client.gencache.EnsureDispatch(prog)
                    self._dispatches[prog] = dispatch
                    if False:  # TODO: 이벤트 처리 관련해서 아직 개발하지 못함
                        handler = win32com.client.WithEvents(
                            dispatch, CybosPlusEventHandler
                        )
                        self._handlers[prog] = handler
        dispatch = self._dispatches[prog]
        return dispatch

    def _GetHandler(self, prog):
        handler = None
        _ = self._EnsureDispatch(prog)
        if prog in self._handlers:
            handler = self._handlers[prog]
        return handler

    def Dispatch(self, request, context):
        prog = request.prog
        dispatch = self._EnsureDispatch(prog)
        properties = [p for p in dispatch._prop_map_get_.keys()]
        methods = [
            m
            for m in dir(dispatch)
            if not m.startswith("_") and m not in ["CLSID", "coclass_clsid"]
        ]
        response = CybosPlusProxyService_pb2.DispatchResponse()
        response.prog = prog
        response.properties.extend(properties)  # pylint: disable=no-member
        response.methods.extend(methods)  # pylint: disable=no-member
        return response

    def Property(self, request, context):
        prog = request.prog
        dispatch = self._EnsureDispatch(prog)
        name = request.name
        value = getattr(dispatch, name)
        response = CybosPlusProxyService_pb2.PropertyResponse()
        AssignPrimitive(response.value, value)  # pylint: disable=no-member
        return response

    def Method(self, request, context):
        prog = request.prog
        dispatch = self._EnsureDispatch(prog)
        name = request.name
        method = getattr(dispatch, name)
        arguments = [ExtractPrimitive(arg.value) for arg in request.arguments]
        return_value = method(*arguments)
        response = CybosPlusProxyService_pb2.MethodResponse()
        AssignPrimitive(
            response.return_value, return_value
        )  # pylint: disable=no-member
        return response

    def Event(self, request_iterator, context):
        start_request = next(request_iterator)
        assert start_request.HasField("start")
        prog = start_request.start.prog
        handler = self._GetHandler(prog)
        response = CybosPlusProxyService_pb2.EventResponse()
        response.started  # pylint: disable=no-member,pointless-statement
        yield response
        for event in handler:
            response = CybosPlusProxyService_pb2.EventResponse()
            response.fired  # pylint: disable=no-member,pointless-statement
            yield response
            done_request = next(request_iterator)
            event.done()
            if done_request.HasField("stop"):
                break
