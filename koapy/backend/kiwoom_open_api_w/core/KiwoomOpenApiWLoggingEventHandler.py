from koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandler import KiwoomOpenApiWEventHandler
from koapy.utils.logging.Logging import Logging

class KiwoomOpenApiWLoggingEventHandler(KiwoomOpenApiWEventHandler, Logging):

    def OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext):
        self.logger.debug('OnReceiveTrData(%r, %r, %r, %r, %r)', scrnno, rqname, trcode, recordname, prevnext)

    def OnReceiveRealData(self, code, realtype, realdata):
        self.logger.debug('OnReceiveRealData(%r, %r, %r)', code, realtype, realdata)

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        self.logger.debug('OnReceiveMsg(%r, %r, %r, %r)', scrnno, rqname, trcode, msg)

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        self.logger.debug('OnReceiveChejanData(%r, %r, %r)', gubun, itemcnt, fidlist)

    def OnEventConnect(self, errcode):
        self.logger.debug('OnEventConnect(%r)', errcode)
