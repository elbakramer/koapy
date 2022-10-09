from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Any, Callable, Optional

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

import grpc

from koapy.backend.daishin_cybos_plus.stub import (
    CpForeDib,
    CpForeTrade,
    CpSysDib,
    CpTrade,
    CpUtil,
    DsCbo1,
)
from koapy.common import DispatchProxyService_pb2, DispatchProxyService_pb2_grpc
from koapy.common.DispatchProxyServiceMessageUtils import AssignValue, ExtractValue
from koapy.common.EventInstance import EventInstance
from koapy.utils.logging.Logging import Logging

P = ParamSpec("P")

CLSIDToClassMap = {
    str(getattr(mod, name).CLSID): getattr(mod, name)
    for mod in [
        CpForeDib,
        CpForeTrade,
        CpSysDib,
        CpTrade,
        CpUtil,
        DsCbo1,
    ]
    for name in dir(mod)
    if hasattr(getattr(mod, name), "CLSID")
}


class CybosPlusDispatchProxyMethod:
    def __init__(self, proxy, name):
        self._proxy = proxy
        self._name = name

    def __call__(self, *args, **kwargs):
        return self._proxy._CallMethod(self._name, args)


class CybosPlusDispatchProxyEventInstance(EventInstance[P]):
    def __init__(self, proxy, name):
        super().__init__()
        self._proxy = proxy
        self._name = name

        self._future = None

    def connect(self, slot: Callable[P, Any]):
        with self._lock:
            if slot not in self._slots:
                self._slots.append(slot)

            if len(self._slots) > 0 and self._future is None:
                self._future, _ = self._proxy._ConnectEvent(self._name)

    def disconnect(self, slot: Optional[Callable[P, Any]] = None):
        super().disconnect(slot)


class CybosPlusDispatchProxy(Logging):
    def __init__(
        self,
        iid: str,
        stub: DispatchProxyService_pb2_grpc.DispatchProxyServiceStub,
        timeout: Optional[int] = None,
        max_workers: Optional[int] = None,
    ):
        self._iid = iid
        self._stub = stub

        self._timeout = timeout
        self._max_workers = max_workers

        self._class = CLSIDToClassMap[self._iid]

        self._properties = [
            name
            for name in dir(self._class)
            if isinstance(getattr(self._class, name), property)
            and not name.startswith("On")
        ]
        self._methods = [
            name
            for name in dir(self._class)
            if hasattr(getattr(self._class, name), "__call__")
        ]
        self._events = [
            name
            for name in dir(self._class)
            if isinstance(getattr(self._class, name), property)
            and name.startswith("On")
        ]

        self._method_instances = {}
        self._event_instances = {}

        for method in self._methods:
            self._method_instances[method] = CybosPlusDispatchProxyMethod(self, method)

        for event in self._events:
            self._event_instances[event] = CybosPlusDispatchProxyEventInstance(
                self, event
            )

        self._executor = ThreadPoolExecutor(max_workers=self._max_workers)

    def _GetAttr(self, name):
        request = DispatchProxyService_pb2.GetAttrRequest()
        request.iid = self._iid
        request.name = name
        should_stop = False
        while not should_stop:
            try:
                response = self._stub.GetAttr(request, timeout=self._timeout)
            except grpc.RpcError as error:
                # error = typing.cast(grpc.Call, error)
                # pylint: disable=no-member
                if error.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    self.logger.warning(
                        "getattr(self, %r) timed out, retrying...", name
                    )
                else:
                    raise
            else:
                should_stop = True
        result = ExtractValue(response.value)
        return result

    def _SetAttr(self, name, value):
        request = DispatchProxyService_pb2.SetAttrRequest()
        request.iid = self._iid
        request.name = name
        request.value = value
        should_stop = False
        while not should_stop:
            try:
                response = self._stub.SetAttr(request, timeout=self._timeout)
            except grpc.RpcError as error:
                # error = typing.cast(grpc.Call, error)
                # pylint: disable=no-member
                if error.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    self.logger.warning(
                        "setattr(self, %r, %r) timed out, retrying...", name, value
                    )
                else:
                    raise
            else:
                should_stop = True
        return response and None

    def _CallMethod(self, name, args):
        request = DispatchProxyService_pb2.CallMethodRequest()
        request.iid = self._iid
        request.name = name
        for arg in args:
            AssignValue(request.arguments.add().value, arg)
        should_stop = False
        while not should_stop:
            try:
                response = self._stub.CallMethod(request, timeout=self._timeout)
            except grpc.RpcError as error:
                # error = typing.cast(grpc.Call, error)
                # pylint: disable=no-member
                if error.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                    self.logger.warning(
                        "Method call %s(%s) timed out, retrying...",
                        name,
                        ", ".join(map(repr, args)),
                    )
                else:
                    raise
            else:
                should_stop = True
        result = ExtractValue(response.return_value)
        return result

    def _ConnectEvent(self, name):
        request = DispatchProxyService_pb2.ConnectEventRequest()
        request.establish_request.iid = self._iid
        request.establish_request.name = name
        event_instance = self._event_instances[name]
        request_queue = Queue()
        sentinel = object()
        request_iterator = iter(request_queue.get, sentinel)
        request_queue.put(request)

        def put_sentinel():
            request_queue.put(sentinel)

        response_iterator = self._stub.ConnectEvent(request_iterator)

        def submit():
            for response in response_iterator:
                args = [ExtractValue(arg.value) for arg in response.arguments]
                event_instance(*args)
                request = DispatchProxyService_pb2.ConnectEventRequest()
                request.ack_request  # pylint: disable=pointless-statement
                request_queue.put(request)

        future = self._executor.submit(submit)

        return future, put_sentinel

    def __getattr__(self, name):
        if name in self._properties:
            return self._GetAttr(name)
        elif name in self._method_instances:
            return self._method_instances[name]
        elif name in self._event_instances:
            return self._event_instances[name]
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if "_properties" in self.__dict__ and name in self.__dict__["_properties"]:
            self._SetAttr(name, value)
        else:
            super().__setattr__(name, value)
