:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers`
======================================================================================

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




.. py:class:: KiwoomOpenApiPlusLoggingEventHandler(control)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandler.KiwoomOpenApiPlusEventHandler`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)

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


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. py:method:: OnEventConnect(self, errcode)


   .. py:method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. py:method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. py:method:: OnReceiveConditionVer(self, ret, msg)



.. py:class:: KiwoomOpenApiPlusLazyAllEventHandler(control, context)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. py:method:: OnEventConnect(self, errcode)


   .. py:method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. py:method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. py:method:: OnReceiveConditionVer(self, ret, msg)



.. py:class:: KiwoomOpenApiPlusEagerAllEventHandler(control, context)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. py:method:: OnEventConnect(self, errcode)


   .. py:method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. py:method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. py:method:: OnReceiveConditionVer(self, ret, msg)



.. py:class:: KiwoomOpenApiPlusAllEventHandler(control, context)

   Bases: :py:obj:`KiwoomOpenApiPlusEagerAllEventHandler`


.. py:class:: KiwoomOpenApiPlusLazySomeEventHandler(control, request, context)

   Bases: :py:obj:`KiwoomOpenApiPlusLazyAllEventHandler`

   .. py:method:: slots(self)



.. py:class:: KiwoomOpenApiPlusEagerSomeEventHandler(control, request, context)

   Bases: :py:obj:`KiwoomOpenApiPlusEagerAllEventHandler`

   .. py:method:: slots(self)



.. py:class:: KiwoomOpenApiPlusSomeEventHandler(control, request, context)

   Bases: :py:obj:`KiwoomOpenApiPlusEagerSomeEventHandler`


.. py:class:: KiwoomOpenApiPlusSomeBidirectionalEventHandler(control, request_iterator, context)

   Bases: :py:obj:`KiwoomOpenApiPlusLazySomeEventHandler`

   .. py:method:: await_handled(self)


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. py:method:: OnEventConnect(self, errcode)


   .. py:method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. py:method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. py:method:: OnReceiveConditionVer(self, ret, msg)



.. py:class:: KiwoomOpenApiPlusLoginEventHandler(control, request, context)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`

   .. py:method:: on_enter(self)


   .. py:method:: OnEventConnect(self, errcode)



.. py:class:: KiwoomOpenApiPlusTrEventHandler(control, request, context, screen_manager)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. py:method:: OnEventConnect(self, errcode)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)



.. py:class:: KiwoomOpenApiPlusKwTrEventHandler(control, request, context, screen_manager)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. py:method:: OnEventConnect(self, errcode)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)



.. py:class:: KiwoomOpenApiPlusBaseOrderEventHandler(control, context)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: ResponseForOnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. py:method:: ResponseForOnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. py:method:: ResponseForOnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. py:method:: OnEventConnect(self, errcode)



.. py:class:: KiwoomOpenApiPlusAllOrderEventHandler(control, context)

   Bases: :py:obj:`KiwoomOpenApiPlusBaseOrderEventHandler`


.. py:class:: KiwoomOpenApiPlusOrderEventHandler(control, request, context, screen_manager)

   Bases: :py:obj:`KiwoomOpenApiPlusBaseOrderEventHandler`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)



.. py:class:: KiwoomOpenApiPlusRealEventHandler(control, request, context, screen_manager)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:attribute:: _num_codes_per_screen
      :annotation: = 100

      

   .. py:attribute:: _default_opt_type
      :annotation: = 0

      

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)


   .. py:method:: OnEventConnect(self, errcode)



.. py:class:: KiwoomOpenApiPlusLoadConditionEventHandler(control, context, request)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveConditionVer(self, ret, msg)



.. py:class:: KiwoomOpenApiPlusConditionEventHandler(control, request, context, screen_manager)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. py:method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)



.. py:class:: KiwoomOpenApiPlusBidirectionalRealEventHandler(control, request_iterator, context, screen_manager)

   Bases: :py:obj:`KiwoomOpenApiPlusRealEventHandler`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: register_code(self, code, fid_list=None)


   .. py:method:: remove_code(self, code)


   .. py:method:: remove_all_codes(self)


   .. py:method:: remove_all_screens(self)


   .. py:method:: consume_request_iterator(self)


   .. py:method:: stop_request_iterator_consumer(self)


   .. py:method:: start_request_iterator_consumer(self)


   .. py:method:: on_enter(self)


   .. py:method:: on_exit(self, exc_type=None, exc_value=None, traceback=None)


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)



