import threading

from koapy.grpc import KiwoomOpenApiService_pb2, KiwoomOpenApiService_pb2_grpc
from koapy.grpc.event.BaseKiwoomOpenApiEventHandler import BaseKiwoomOpenApiEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandler import KiwoomOpenApiAllEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandler import KiwoomOpenApiSomeEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandler import KiwoomOpenApiLoginEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandler import KiwoomOpenApiTrEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandler import KiwoomOpenApiOrderEventHandler
from koapy.grpc.event.KiwoomOpenApiEventHandler import KiwoomOpenApiRealEventHandler
from koapy.openapi.KiwoomOpenApiError import KiwoomOpenApiError

from koapy.utils.itertools import chunk

class KiwoomOpenApiServiceServicer(KiwoomOpenApiService_pb2_grpc.KiwoomOpenApiServiceServicer):

    _listen_id_to_handler = {}
    _listen_id_to_handler_lock = threading.RLock()

    def __init__(self, control):
        super().__init__()
        self._control = control

    @property
    def control(self):
        return self._control

    @classmethod
    def _convertArguments(cls, arguments):
        args = []
        for argument in arguments:
            if argument.HasField('string_value'):
                args.append(argument.string_value)
            elif argument.HasField('long_value'):
                args.append(argument.long_value)
        return args

    def Call(self, request, context):
        name = request.name
        arguments = self._convertArguments(request.arguments)
        function = getattr(self.control, name)
        result = function(*arguments)
        response = KiwoomOpenApiService_pb2.CallResponse()
        if isinstance(result, str):
            response.return_value.string_value = result # pylint: disable=no-member
        elif isinstance(result, int):
            response.return_value.long_value = result # pylint: disable=no-member
        elif result is None:
            pass
        else:
            raise TypeError('Unexpected return value type from server side dynamicCall(): %s' % type(result))
        return response

    def _RegisterHandler(self, id, handler):
        with self._listen_id_to_handler_lock:
            self._UnregisterHandler(id)
            self._listen_id_to_handler[id] = handler

    def _UnregisterHandler(self, id):
        with self._listen_id_to_handler_lock:
            if id in self._listen_id_to_handler:
                self._listen_id_to_handler[id].observer.on_completed()
                del self._listen_id_to_handler[id]
                return True
        return False

    def Listen(self, request, context):
        handler = KiwoomOpenApiSomeEventHandler(self.control, request)
        self._RegisterHandler(request.id, handler)
        handler.add_callback(self._UnregisterHandler, request.id)
        with handler:
            for response in handler:
                yield response

    def StopListen(self, request, context):
        response = KiwoomOpenApiService_pb2.StopListenResponse()
        response.successful = self._UnregisterHandler(request.id)
        return response

    def CustomListen(self, request, context):
        code = request.code
        class_name = request.class_name
        if code and class_name:
            g = {}
            l = {}
            exec(code, g, l)
            handler = eval(class_name, g, l)(self.control, request)
            assert isinstance(handler, BaseKiwoomOpenApiEventHandler)
            with handler:
                for response in handler:
                    yield response
        else:
            handler = KiwoomOpenApiAllEventHandler(self.control)
            with handler:
                for response in handler:
                    yield response

    def CustomCallAndListen(self, request, context):
        name = request.name
        arguments = self._convertArguments(request.arguments)
        function = getattr(self.control, name)
        code = request.listen_request.code
        class_name = request.listen_request.class_name
        if code and class_name:
            g = {}
            l = {}
            exec(code, g, l)
            handler = eval(class_name, g, l)(self.control, request)
            assert isinstance(handler, BaseKiwoomOpenApiEventHandler)
        else:
            handler = KiwoomOpenApiAllEventHandler(self.control)
        with handler:
            result = function(*arguments)
            response = KiwoomOpenApiService_pb2.CustomCallAndListenResponse()
            if isinstance(result, str):
                response.call_response.return_value.string_value = result # pylint: disable=no-member
            elif isinstance(result, int):
                response.call_response.return_value.long_value = result # pylint: disable=no-member
            elif result is None:
                pass
            else:
                raise TypeError('Unexpected return value type from server side dynamicCall(): %s' % type(result))
            yield response
            for response in handler:
                yield response

    def LoginCall(self, request, context):
        with KiwoomOpenApiLoginEventHandler(self.control, request) as handler:
            KiwoomOpenApiError.try_or_raise(
                self.control.CommConnect())
            for response in handler:
                yield response

    def TransactionCall(self, request, context):
        rqname = request.request_name
        trcode = request.transaction_code
        prevnext = 0
        scrnno = request.screen_no
        inputs = request.inputs
        with KiwoomOpenApiTrEventHandler(self.control, request) as handler:
            for k, v in inputs.items():
                self.control.SetInputValue(k, v)
            KiwoomOpenApiError.try_or_raise(
                self.control.RateLimitedCommRqData(rqname, trcode, int(prevnext), scrnno, inputs))
            for response in handler:
                yield response

    def OrderCall(self, request, context):
        rqname = request.request_name
        scrnno = request.screen_no
        accno = request.account_no
        ordertype = request.order_type
        code = request.code
        qty = request.quantity
        price = request.price
        hogagb = request.quote_type
        orgorderno = request.original_order_no
        with KiwoomOpenApiOrderEventHandler(self.control, request) as handler:
            KiwoomOpenApiError.try_or_raise(
                self.control.SendOrder(rqname, scrnno, accno, ordertype, code, qty, price, hogagb, orgorderno))
            for response in handler:
                yield response

    def RealCall(self, request, context):
        code_lists = [';'.join(codes) for codes in chunk(request.code_list, 100)]
        screen_nos = [str(int(request.screen_no or '0001') + i).zfill(4) for i in range(len(code_lists))]
        fid_list = ';'.join([str(fid) for fid in request.fid_list])
        real_type = request.real_type or '0'
        with KiwoomOpenApiRealEventHandler(self.control, request) as handler:
            for screen_no, code_list in zip(screen_nos, code_lists):
                handler.add_callback(self.control.DisconnectRealData, screen_no)
                handler.add_callback(self.control.SetRealRemove, screen_no, 'ALL')
                KiwoomOpenApiError.try_or_raise(
                    self.control.SetRealReg(screen_no, code_list, fid_list, real_type))
            for response in handler:
                yield response
