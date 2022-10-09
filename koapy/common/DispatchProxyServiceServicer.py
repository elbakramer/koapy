import atexit

from queue import Queue
from typing import Iterator, Union

from grpc import ServicerContext
from pywintypes import IID

from koapy.common import DispatchProxyService_pb2, DispatchProxyService_pb2_grpc
from koapy.common.Dispatch import Dispatch
from koapy.common.DispatchProxyServiceMessageUtils import AssignValue, ExtractValue
from koapy.common.EventInstance import EventInstance


class DispatchProxyServiceServicer(
    DispatchProxyService_pb2_grpc.DispatchProxyServiceServicer
):
    def _GetDispatch(self, iid: Union[IID, str]) -> Dispatch:
        return Dispatch(iid)

    def GetDispatch(
        self,
        request: DispatchProxyService_pb2.GetDispatchRequest,
        context: ServicerContext,
    ) -> DispatchProxyService_pb2.GetDispatchResponse:
        iid = request.iid
        iid = IID(iid)
        iid = str(iid)
        response = DispatchProxyService_pb2.GetDispatchResponse()
        response.iid = iid
        return response

    def GetAttr(
        self,
        request: DispatchProxyService_pb2.GetAttrRequest,
        context: ServicerContext,
    ) -> DispatchProxyService_pb2.GetAttrResponse:
        iid = request.iid
        name = request.name
        dispatch = self._GetDispatch(iid)
        value = getattr(dispatch, name)
        response = DispatchProxyService_pb2.GetAttrResponse()
        AssignValue(response.value, value)
        return response

    def SetAttr(
        self,
        request: DispatchProxyService_pb2.SetAttrRequest,
        context: ServicerContext,
    ) -> DispatchProxyService_pb2.SetAttrResponse:
        iid = request.iid
        name = request.name
        value = request.value
        dispatch = self._GetDispatch(iid)
        setattr(dispatch, name, value)
        response = DispatchProxyService_pb2.SetAttrResponse()
        return response

    def CallMethod(
        self,
        request: DispatchProxyService_pb2.CallMethodRequest,
        context: ServicerContext,
    ) -> DispatchProxyService_pb2.CallMethodResponse:
        iid = request.iid
        name = request.name
        arguments = request.arguments
        arguments = [ExtractValue(arg.value) for arg in arguments]
        dispatch = self._GetDispatch(iid)
        method = getattr(dispatch, name)
        return_value = method(*arguments)
        response = DispatchProxyService_pb2.CallMethodResponse()
        AssignValue(response.return_value, return_value)
        return response

    def ConnectEvent(
        self,
        request_iterator: Iterator[DispatchProxyService_pb2.ConnectEventRequest],
        context: ServicerContext,
    ) -> Iterator[DispatchProxyService_pb2.ConnectEventResponse]:
        request = next(request_iterator)
        assert request.HasField("establish_request")

        request = request.establish_request
        iid = request.iid
        iid = IID(iid)
        iid = str(iid)
        name = request.name
        dispatch = self._GetDispatch(iid)
        event_instance: EventInstance = getattr(dispatch, name)
        queue = Queue()
        sentinel = object()

        def slot(*args, **_kwargs):
            queue.put(args)
            request = next(request_iterator)
            assert request.HasField("ack_request")

        def put_sentinel():
            queue.put(sentinel)

        def callback():
            event_instance.disconnect(slot)
            atexit.unregister(put_sentinel)
            queue.put(sentinel)

        context.add_callabck(callback)
        atexit.register(put_sentinel)
        event_instance.connect(slot)

        for args in iter(queue.get, sentinel):
            response = DispatchProxyService_pb2.ConnectEventResponse()
            response.iid = iid
            response.name = name
            for arg in args:
                AssignValue(response.arguments.add().value, arg)
            queue.task_done()
            yield response
