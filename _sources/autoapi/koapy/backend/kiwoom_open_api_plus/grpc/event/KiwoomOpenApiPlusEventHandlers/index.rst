:mod:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers`
===================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusLoggingEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusLazyAllEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusEagerAllEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusAllEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusLazySomeEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusEagerSomeEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusSomeEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusSomeBidirectionalEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusLoginEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusTrEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusKwTrEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusBaseOrderEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusAllOrderEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusOrderEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusRealEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusLoadConditionEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusConditionEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusBidirectionalRealEventHandler




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



.. class:: KiwoomOpenApiPlusLazyAllEventHandler(control, context)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)


   .. method:: OnReceiveRealData(self, code, realtype, realdata)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. method:: OnEventConnect(self, errcode)


   .. method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. method:: OnReceiveConditionVer(self, ret, msg)



.. class:: KiwoomOpenApiPlusEagerAllEventHandler(control, context)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)


   .. method:: OnReceiveRealData(self, code, realtype, realdata)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. method:: OnEventConnect(self, errcode)


   .. method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. method:: OnReceiveConditionVer(self, ret, msg)



.. class:: KiwoomOpenApiPlusAllEventHandler(control, context)


   Bases: :py:obj:`KiwoomOpenApiPlusEagerAllEventHandler`


.. class:: KiwoomOpenApiPlusLazySomeEventHandler(control, request, context)


   Bases: :py:obj:`KiwoomOpenApiPlusLazyAllEventHandler`

   .. method:: slots(self)



.. class:: KiwoomOpenApiPlusEagerSomeEventHandler(control, request, context)


   Bases: :py:obj:`KiwoomOpenApiPlusEagerAllEventHandler`

   .. method:: slots(self)



.. class:: KiwoomOpenApiPlusSomeEventHandler(control, request, context)


   Bases: :py:obj:`KiwoomOpenApiPlusEagerSomeEventHandler`


.. class:: KiwoomOpenApiPlusSomeBidirectionalEventHandler(control, request_iterator, context)


   Bases: :py:obj:`KiwoomOpenApiPlusLazySomeEventHandler`

   .. method:: await_handled(self)


   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)


   .. method:: OnReceiveRealData(self, code, realtype, realdata)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. method:: OnEventConnect(self, errcode)


   .. method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. method:: OnReceiveConditionVer(self, ret, msg)



.. class:: KiwoomOpenApiPlusLoginEventHandler(control, request, context)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`

   .. method:: on_enter(self)


   .. method:: OnEventConnect(self, errcode)



.. class:: KiwoomOpenApiPlusTrEventHandler(control, request, context, screen_manager)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: on_enter(self)


   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. method:: OnEventConnect(self, errcode)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)



.. class:: KiwoomOpenApiPlusKwTrEventHandler(control, request, context, screen_manager)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: on_enter(self)


   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. method:: OnEventConnect(self, errcode)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)



.. class:: KiwoomOpenApiPlusBaseOrderEventHandler(control, context)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: ResponseForOnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. method:: ResponseForOnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. method:: ResponseForOnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. method:: OnEventConnect(self, errcode)



.. class:: KiwoomOpenApiPlusAllOrderEventHandler(control, context)


   Bases: :py:obj:`KiwoomOpenApiPlusBaseOrderEventHandler`


.. class:: KiwoomOpenApiPlusOrderEventHandler(control, request, context, screen_manager)


   Bases: :py:obj:`KiwoomOpenApiPlusBaseOrderEventHandler`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: on_enter(self)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)



.. class:: KiwoomOpenApiPlusRealEventHandler(control, request, context, screen_manager)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: _num_codes_per_screen
      :annotation: = 100

      

   .. attribute:: _default_real_type
      :annotation: = 0

      

   .. method:: on_enter(self)


   .. method:: OnReceiveRealData(self, code, realtype, realdata)


   .. method:: OnEventConnect(self, errcode)



.. class:: KiwoomOpenApiPlusLoadConditionEventHandler(control, context, request)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`

   .. method:: on_enter(self)


   .. method:: OnReceiveConditionVer(self, ret, msg)



.. class:: KiwoomOpenApiPlusConditionEventHandler(control, request, context, screen_manager)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: on_enter(self)


   .. method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)



.. class:: KiwoomOpenApiPlusBidirectionalRealEventHandler(control, request_iterator, context, screen_manager)


   Bases: :py:obj:`KiwoomOpenApiPlusRealEventHandler`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: register_code(self, code, fid_list=None)


   .. method:: remove_code(self, code)


   .. method:: remove_all_codes(self)


   .. method:: remove_all_screens(self)


   .. method:: consume_request_iterator(self)


   .. method:: stop_request_iterator_consumer(self)


   .. method:: start_request_iterator_consumer(self)


   .. method:: on_enter(self)


   .. method:: on_exit(self, exc_type=None, exc_value=None, traceback=None)


   .. method:: OnReceiveRealData(self, code, realtype, realdata)



