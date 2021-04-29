import datetime

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandler import (
    KiwoomOpenApiPlusEventHandler,
)
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiPlusLoggingEventHandler(KiwoomOpenApiPlusEventHandler, Logging):
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
        self.logger.debug(
            "OnReceiveTrData(%r, %r, %r, %r, %r)",
            scrnno,
            rqname,
            trcode,
            recordname,
            prevnext,
        )

    def OnReceiveRealData(self, code, realtype, realdata):
        self.logger.debug("OnReceiveRealData(%r, %r, %r)", code, realtype, realdata)
        if code == "09" and realtype == "장시작시간":
            signal_type = self.control.GetCommRealData(code, 215)
            current_time = self.control.GetCommRealData(code, 20)
            estimated_remaining_time = self.control.GetCommRealData(code, 214)
            signal_type_msg = {
                # 아래는 문서에서 확인 가능
                "0": "장시작전(동시호가시작,이후1분단위)",
                "2": "장종료전(동시호가시작,이후1분단위)",
                "3": "장시작(동시호가종료)",
                "4": "장종료(동시호가종료)",
                "8": "장종료(시간내용없음)",
                "9": "장마감(시간내용없음)",
                # 이후는 추정
                "s": "선물옵션장종료전(동시호가시작)",  # 17번반복
                "a": "장후시간외종가시작",
                "e": "선물옵션장종료(동시호가종료)",  # 17번반복
                "b": "장후시간외종가종료",
                "c": "시간외단일가시작",
                "d": "시간외단일가종료",
            }.get(signal_type, "알수없음")
            if signal_type not in ["8", "9"]:
                current_time = datetime.datetime.strptime(current_time, "%H%M%S")
            else:
                current_time = datetime.datetime.now()
            ert = datetime.datetime.strptime(estimated_remaining_time, "%H%M%S")
            estimated_remaining_time = datetime.timedelta(
                hours=ert.hour, minutes=ert.minute, seconds=ert.second
            )
            self.logger.debug(
                "%s, %s remaining", signal_type_msg, estimated_remaining_time
            )

    def OnReceiveMsg(self, scrnno, rqname, trcode, msg):
        """
        [OnReceiveMsg()이벤트]

          OnReceiveMsg(
          BSTR sScrNo,   // 화면번호
          BSTR sRQName,  // 사용자 구분명
          BSTR sTrCode,  // TR이름
          BSTR sMsg     // 서버에서 전달하는 메시지
          )

          서버통신 후 수신한 메시지를 알려줍니다.
          메시지에는 6자리 코드번호가 포함되는데 이 코드번호는 통보없이 수시로 변경될 수 있습니다. 따라서 주문이나 오류관련처리를
          이 코드번호로 분류하시면 안됩니다.
        """
        self.logger.debug("OnReceiveMsg(%r, %r, %r, %r)", scrnno, rqname, trcode, msg)

        if msg == "전문 처리 실패(-22)":
            self.logger.warning("Server might have ended connection abruptly")

    def OnReceiveChejanData(self, gubun, itemcnt, fidlist):
        self.logger.debug("OnReceiveChejanData(%r, %r, %r)", gubun, itemcnt, fidlist)

    def OnEventConnect(self, errcode):
        self.logger.debug("OnEventConnect(%r)", errcode)

    def OnReceiveRealCondition(
        self, code, condition_type, condition_name, condition_index
    ):
        self.logger.debug(
            "OnReceiveRealCondition(%r, %r, %r, %r)",
            code,
            condition_type,
            condition_name,
            condition_index,
        )

    def OnReceiveTrCondition(
        self, scrnno, codelist, condition_name, condition_index, prevnext
    ):
        self.logger.debug(
            "OnReceiveTrCondition(%r, %r, %r, %r, %r)",
            scrnno,
            codelist,
            condition_name,
            condition_index,
            prevnext,
        )

    def OnReceiveConditionVer(self, ret, msg):
        self.logger.debug("OnReceiveConditionVer(%r, %r)", ret, msg)
