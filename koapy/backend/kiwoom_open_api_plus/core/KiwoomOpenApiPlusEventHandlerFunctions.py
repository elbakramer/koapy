from koapy.utils.notimplemented import notimplemented

class KiwoomOpenApiPlusEventHandlerFunctions:

    @notimplemented
    def OnEventConnect(self, errcode):
        raise NotImplementedError

    @notimplemented
    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        raise NotImplementedError

    @notimplemented
    def OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg):
        raise NotImplementedError

    @notimplemented
    def OnReceiveRealData(self, code, realtype, realdata):
        raise NotImplementedError

    @notimplemented
    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        raise NotImplementedError

    @notimplemented
    def OnReceiveConditionVer(self, ret, msg):
        raise NotImplementedError

    @notimplemented
    def OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext):
        raise NotImplementedError

    @notimplemented
    def OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index):
        raise NotImplementedError
