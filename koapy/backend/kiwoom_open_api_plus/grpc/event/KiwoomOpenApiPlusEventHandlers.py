from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType import (
    KiwoomOpenApiPlusRealType,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo import (
    KiwoomOpenApiPlusTrInfo,
)
from koapy.backend.kiwoom_open_api_plus.grpc import KiwoomOpenApiPlusService_pb2
from koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc import (
    KiwoomOpenApiPlusEventHandlerForGrpc,
)
from koapy.utils.logging.Logging import Logging
from koapy.utils.notimplemented import isimplemented


class KiwoomOpenApiPlusLazyAllEventHandler(
    KiwoomOpenApiPlusEventHandlerForGrpc, Logging
):
    def OnReceiveTrData(
        self,
        scrnno,
        rqname,
        trcode,
        recordname,
        prevnext,
        _datalength,
        _errorcode,
        _message,
        _splmmsg,
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveTrData"
        response.arguments.add().string_value = scrnno
        response.arguments.add().string_value = rqname
        response.arguments.add().string_value = trcode
        response.arguments.add().string_value = recordname
        response.arguments.add().string_value = prevnext
        self.observer.on_next(response)

    def OnReceiveRealData(self, code, realtype, realdata):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveRealData"
        response.arguments.add().string_value = code
        response.arguments.add().string_value = realtype
        response.arguments.add().string_value = realdata
        self.observer.on_next(response)

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveMsg"
        response.arguments.add().string_value = scrnno
        response.arguments.add().string_value = rqname
        response.arguments.add().string_value = trcode
        response.arguments.add().string_value = msg
        self.observer.on_next(response)

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveChejanData"
        response.arguments.add().string_value = gubun
        response.arguments.add().long_value = itemcnt
        response.arguments.add().string_value = fidlist
        self.observer.on_next(response)

    def OnEventConnect(self, errcode):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnEventConnect"
        response.arguments.add().long_value = errcode
        self.observer.on_next(response)

    def OnReceiveRealCondition(
        self, code, condition_type, condition_name, condition_index
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveRealCondition"
        response.arguments.add().string_value = code
        response.arguments.add().string_value = condition_type
        response.arguments.add().string_value = condition_name
        response.arguments.add().string_value = condition_index
        self.observer.on_next(response)

    def OnReceiveTrCondition(
        self, scrnno, codelist, condition_name, condition_index, prevnext
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveTrCondition"
        response.arguments.add().string_value = scrnno
        response.arguments.add().string_value = codelist
        response.arguments.add().string_value = condition_name
        response.arguments.add().long_value = condition_index
        response.arguments.add().long_value = prevnext
        self.observer.on_next(response)

    def OnReceiveConditionVer(self, ret, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveConditionVer"
        response.arguments.add().long_value = ret
        response.arguments.add().string_value = msg
        self.observer.on_next(response)


class KiwoomOpenApiPlusEagerAllEventHandler(
    KiwoomOpenApiPlusEventHandlerForGrpc, Logging
):
    def OnReceiveTrData(
        self,
        scrnno,
        rqname,
        trcode,
        recordname,
        prevnext,
        _datalength,
        _errorcode,
        _message,
        _splmmsg,
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveTrData"
        response.arguments.add().string_value = scrnno
        response.arguments.add().string_value = rqname
        response.arguments.add().string_value = trcode
        response.arguments.add().string_value = recordname
        response.arguments.add().string_value = prevnext

        repeat_cnt = self.control.GetRepeatCnt(trcode, recordname)

        trinfo = KiwoomOpenApiPlusTrInfo.get_trinfo_by_code(trcode)

        if trinfo is None:
            self.logger.error("Cannot find names for trcode %s", trinfo)

        single_names = trinfo.get_single_output_names()
        multi_names = trinfo.get_multi_output_names()

        if len(single_names) > 0:
            values = [
                self.control.GetCommData(trcode, recordname, 0, name).strip()
                for name in single_names
            ]
            response.single_data.names.extend(single_names)
            response.single_data.values.extend(values)

        if repeat_cnt > 0 and len(multi_names) > 0:
            rows = [
                [
                    self.control.GetCommData(trcode, recordname, i, name).strip()
                    for name in multi_names
                ]
                for i in range(repeat_cnt)
            ]
            response.multi_data.names.extend(multi_names)
            for row in rows:
                response.multi_data.values.add().values.extend(row)

        self.observer.on_next(response)

    def OnReceiveRealData(self, code, realtype, realdata):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveRealData"
        response.arguments.add().string_value = code
        response.arguments.add().string_value = realtype
        response.arguments.add().string_value = realdata

        fids = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name(realtype)

        if fids is None:
            self.logger.error("Cannot find fids for realtype %s", realtype)

        names = [
            KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids
        ]
        values = [self.control.GetCommRealData(code, fid) for fid in fids]

        assert len(names) == len(values)

        response.single_data.names.extend(names)
        response.single_data.values.extend(values)

        self.observer.on_next(response)

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveMsg"
        response.arguments.add().string_value = scrnno
        response.arguments.add().string_value = rqname
        response.arguments.add().string_value = trcode
        response.arguments.add().string_value = msg
        self.observer.on_next(response)

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveChejanData"
        response.arguments.add().string_value = gubun
        response.arguments.add().long_value = itemcnt
        response.arguments.add().string_value = fidlist

        fids = fidlist.rstrip(";")
        fids = fids.split(";") if fids else []
        fids = [int(fid) for fid in fids]

        assert itemcnt == len(fids)

        names = [
            KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids
        ]
        values = [self.control.GetChejanData(fid).strip() for fid in fids]

        response.single_data.names.extend(names)
        response.single_data.values.extend(values)

        self.observer.on_next(response)

    def OnEventConnect(self, errcode):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnEventConnect"
        response.arguments.add().long_value = errcode
        self.observer.on_next(response)

    def OnReceiveRealCondition(
        self, code, condition_type, condition_name, condition_index
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveRealCondition"
        response.arguments.add().string_value = code
        response.arguments.add().string_value = condition_type
        response.arguments.add().string_value = condition_name
        response.arguments.add().string_value = condition_index
        self.observer.on_next(response)

    def OnReceiveTrCondition(
        self, scrnno, codelist, condition_name, condition_index, prevnext
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveTrCondition"
        response.arguments.add().string_value = scrnno
        response.arguments.add().string_value = codelist
        response.arguments.add().string_value = condition_name
        response.arguments.add().long_value = condition_index
        response.arguments.add().long_value = prevnext
        self.observer.on_next(response)

    def OnReceiveConditionVer(self, ret, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveConditionVer"
        response.arguments.add().long_value = ret
        response.arguments.add().string_value = msg
        self.observer.on_next(response)


class KiwoomOpenApiPlusAllEventHandler(KiwoomOpenApiPlusEagerAllEventHandler):

    pass


class KiwoomOpenApiPlusLazySomeEventHandler(KiwoomOpenApiPlusLazyAllEventHandler):
    def __init__(self, control, request, context):
        super().__init__(control, context)
        self._request = request

    def slots(self):
        names = self.names()
        slots = [getattr(self, name) for name in names]
        names_and_slots_implemented = [
            (name, slot)
            for name, slot in zip(names, slots)
            if isimplemented(slot) and name in self._request.slots
        ]
        return names_and_slots_implemented


class KiwoomOpenApiPlusEagerSomeEventHandler(KiwoomOpenApiPlusEagerAllEventHandler):
    def __init__(self, control, request, context):
        super().__init__(control, context)
        self._request = request

    def slots(self):
        names = self.names()
        slots = [getattr(self, name) for name in names]
        names_and_slots_implemented = [
            (name, slot)
            for name, slot in zip(names, slots)
            if isimplemented(slot) and name in self._request.slots
        ]
        return names_and_slots_implemented


class KiwoomOpenApiPlusSomeEventHandler(KiwoomOpenApiPlusEagerSomeEventHandler):

    pass


class KiwoomOpenApiPlusSomeBidirectionalEventHandler(
    KiwoomOpenApiPlusLazySomeEventHandler
):
    def __init__(self, control, request_iterator, context):
        self._request_iterator = request_iterator
        self._first_request = next(self._request_iterator)
        assert self._first_request.HasField("listen_request")
        self._request = request = self._first_request.listen_request
        super().__init__(control, request, context)

    def await_handled(self):
        request = next(self._request_iterator)
        if request.HasField("handled_request"):
            pass
        elif request.HasField("stop_listen_request"):
            self.observer.on_completed()
        else:
            raise KiwoomOpenApiPlusError("Unexpected request")

    def OnReceiveTrData(
        self,
        scrnno,
        rqname,
        trcode,
        recordname,
        prevnext,
        _datalength,
        _errorcode,
        _message,
        _splmmsg,
    ):
        super().OnReceiveTrData(
            scrnno,
            rqname,
            trcode,
            recordname,
            prevnext,
            _datalength,
            _errorcode,
            _message,
            _splmmsg,
        )
        self.await_handled()

    def OnReceiveRealData(self, code, realtype, realdata):
        super().OnReceiveRealData(code, realtype, realdata)
        self.await_handled()

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        super().OnReceiveMsg(scrnno, rqname, trcode, msg)
        self.await_handled()

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        super().OnReceiveChejanData(gubun, itemcnt, fidlist)
        self.await_handled()

    def OnEventConnect(self, errcode):
        super().OnEventConnect(errcode)
        self.await_handled()

    def OnReceiveRealCondition(
        self, code, condition_type, condition_name, condition_index
    ):
        super().OnReceiveRealCondition(
            code, condition_type, condition_name, condition_index
        )
        self.await_handled()

    def OnReceiveTrCondition(
        self, scrnno, codelist, condition_name, condition_index, prevnext
    ):
        super().OnReceiveTrCondition(
            scrnno, codelist, condition_name, condition_index, prevnext
        )
        self.await_handled()

    def OnReceiveConditionVer(self, ret, msg):
        super().OnReceiveConditionVer(ret, msg)
        self.await_handled()
