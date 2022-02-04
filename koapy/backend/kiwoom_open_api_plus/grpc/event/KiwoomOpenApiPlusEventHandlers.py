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
        response.name = "OnReceiveTrData"  # pylint: disable=no-member
        response.arguments.add().string_value = scrnno  # pylint: disable=no-member
        response.arguments.add().string_value = rqname  # pylint: disable=no-member
        response.arguments.add().string_value = trcode  # pylint: disable=no-member
        response.arguments.add().string_value = recordname  # pylint: disable=no-member
        response.arguments.add().string_value = prevnext  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnReceiveRealData(self, code, realtype, realdata):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveRealData"  # pylint: disable=no-member
        response.arguments.add().string_value = code  # pylint: disable=no-member
        response.arguments.add().string_value = realtype  # pylint: disable=no-member
        response.arguments.add().string_value = realdata  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveMsg"  # pylint: disable=no-member
        response.arguments.add().string_value = scrnno  # pylint: disable=no-member
        response.arguments.add().string_value = rqname  # pylint: disable=no-member
        response.arguments.add().string_value = trcode  # pylint: disable=no-member
        response.arguments.add().string_value = msg  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveChejanData"  # pylint: disable=no-member
        response.arguments.add().string_value = gubun  # pylint: disable=no-member
        response.arguments.add().long_value = itemcnt  # pylint: disable=no-member
        response.arguments.add().string_value = fidlist  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnEventConnect(self, errcode):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnEventConnect"  # pylint: disable=no-member
        response.arguments.add().long_value = errcode  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnReceiveRealCondition(
        self, code, condition_type, condition_name, condition_index
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveRealCondition"  # pylint: disable=no-member
        response.arguments.add().string_value = code  # pylint: disable=no-member
        response.arguments.add().string_value = (
            condition_type  # pylint: disable=no-member
        )
        response.arguments.add().string_value = (
            condition_name  # pylint: disable=no-member
        )
        response.arguments.add().string_value = (
            condition_index  # pylint: disable=no-member
        )
        self.observer.on_next(response)

    def OnReceiveTrCondition(
        self, scrnno, codelist, condition_name, condition_index, prevnext
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveTrCondition"  # pylint: disable=no-member
        response.arguments.add().string_value = scrnno  # pylint: disable=no-member
        response.arguments.add().string_value = codelist  # pylint: disable=no-member
        response.arguments.add().string_value = (
            condition_name  # pylint: disable=no-member
        )
        response.arguments.add().long_value = (
            condition_index  # pylint: disable=no-member
        )
        response.arguments.add().long_value = prevnext  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnReceiveConditionVer(self, ret, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveConditionVer"  # pylint: disable=no-member
        response.arguments.add().long_value = ret  # pylint: disable=no-member
        response.arguments.add().string_value = msg  # pylint: disable=no-member
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
        response.name = "OnReceiveTrData"  # pylint: disable=no-member
        response.arguments.add().string_value = scrnno  # pylint: disable=no-member
        response.arguments.add().string_value = rqname  # pylint: disable=no-member
        response.arguments.add().string_value = trcode  # pylint: disable=no-member
        response.arguments.add().string_value = recordname  # pylint: disable=no-member
        response.arguments.add().string_value = prevnext  # pylint: disable=no-member

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
            response.single_data.names.extend(single_names)  # pylint: disable=no-member
            response.single_data.values.extend(values)  # pylint: disable=no-member

        if repeat_cnt > 0 and len(multi_names) > 0:
            rows = [
                [
                    self.control.GetCommData(trcode, recordname, i, name).strip()
                    for name in multi_names
                ]
                for i in range(repeat_cnt)
            ]
            response.multi_data.names.extend(multi_names)  # pylint: disable=no-member
            for row in rows:
                response.multi_data.values.add().values.extend(
                    row
                )  # pylint: disable=no-member

        self.observer.on_next(response)

    def OnReceiveRealData(self, code, realtype, realdata):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveRealData"  # pylint: disable=no-member
        response.arguments.add().string_value = code  # pylint: disable=no-member
        response.arguments.add().string_value = realtype  # pylint: disable=no-member
        response.arguments.add().string_value = realdata  # pylint: disable=no-member

        fids = KiwoomOpenApiPlusRealType.get_fids_by_realtype_name(realtype)

        if fids is None:
            self.logger.error("Cannot find fids for realtype %s", realtype)

        names = [
            KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids
        ]
        values = [self.control.GetCommRealData(code, fid) for fid in fids]

        assert len(names) == len(values)

        response.single_data.names.extend(names)  # pylint: disable=no-member
        response.single_data.values.extend(values)  # pylint: disable=no-member

        self.observer.on_next(response)

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveMsg"  # pylint: disable=no-member
        response.arguments.add().string_value = scrnno  # pylint: disable=no-member
        response.arguments.add().string_value = rqname  # pylint: disable=no-member
        response.arguments.add().string_value = trcode  # pylint: disable=no-member
        response.arguments.add().string_value = msg  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveChejanData"  # pylint: disable=no-member
        response.arguments.add().string_value = gubun  # pylint: disable=no-member
        response.arguments.add().long_value = itemcnt  # pylint: disable=no-member
        response.arguments.add().string_value = fidlist  # pylint: disable=no-member

        fids = fidlist.rstrip(";")
        fids = fids.split(";") if fids else []
        fids = [int(fid) for fid in fids]

        assert itemcnt == len(fids)

        names = [
            KiwoomOpenApiPlusRealType.Fid.get_name_by_fid(fid, str(fid)) for fid in fids
        ]
        values = [self.control.GetChejanData(fid).strip() for fid in fids]

        response.single_data.names.extend(names)  # pylint: disable=no-member
        response.single_data.values.extend(values)  # pylint: disable=no-member

        self.observer.on_next(response)

    def OnEventConnect(self, errcode):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnEventConnect"  # pylint: disable=no-member
        response.arguments.add().long_value = errcode  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnReceiveRealCondition(
        self, code, condition_type, condition_name, condition_index
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveRealCondition"  # pylint: disable=no-member
        response.arguments.add().string_value = code  # pylint: disable=no-member
        response.arguments.add().string_value = (
            condition_type  # pylint: disable=no-member
        )
        response.arguments.add().string_value = (
            condition_name  # pylint: disable=no-member
        )
        response.arguments.add().string_value = (
            condition_index  # pylint: disable=no-member
        )
        self.observer.on_next(response)

    def OnReceiveTrCondition(
        self, scrnno, codelist, condition_name, condition_index, prevnext
    ):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveTrCondition"  # pylint: disable=no-member
        response.arguments.add().string_value = scrnno  # pylint: disable=no-member
        response.arguments.add().string_value = codelist  # pylint: disable=no-member
        response.arguments.add().string_value = (
            condition_name  # pylint: disable=no-member
        )
        response.arguments.add().long_value = (
            condition_index  # pylint: disable=no-member
        )
        response.arguments.add().long_value = prevnext  # pylint: disable=no-member
        self.observer.on_next(response)

    def OnReceiveConditionVer(self, ret, msg):
        response = KiwoomOpenApiPlusService_pb2.ListenResponse()
        response.name = "OnReceiveConditionVer"  # pylint: disable=no-member
        response.arguments.add().long_value = ret  # pylint: disable=no-member
        response.arguments.add().string_value = msg  # pylint: disable=no-member
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
