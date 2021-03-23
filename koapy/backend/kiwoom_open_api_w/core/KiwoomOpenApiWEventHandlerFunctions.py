from koapy.utils.notimplemented import notimplemented

class KiwoomOpenApiWEventHandlerFunctions:

    @notimplemented
    def OnEventConnect(self, errcode):
        raise NotImplementedError

    @notimplemented
    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        raise NotImplementedError

    @notimplemented
    def OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext):
        raise NotImplementedError

    @notimplemented
    def OnReceiveRealData(self, code, realtype, realdata):
        raise NotImplementedError

    @notimplemented
    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        raise NotImplementedError
