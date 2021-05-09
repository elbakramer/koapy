:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusLoggingEventHandler`
===================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusLoggingEventHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusLoggingEventHandler.KiwoomOpenApiPlusLoggingEventHandler




.. class:: KiwoomOpenApiPlusLoggingEventHandler(control)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandler.KiwoomOpenApiPlusEventHandler`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)


   .. method:: OnReceiveRealData(self, code, realtype, realdata)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)

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


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. method:: OnEventConnect(self, errcode)


   .. method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. method:: OnReceiveConditionVer(self, ret, msg)



