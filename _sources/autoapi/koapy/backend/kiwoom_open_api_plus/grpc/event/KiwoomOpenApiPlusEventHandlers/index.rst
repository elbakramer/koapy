:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers`
======================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusLazyAllEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusEagerAllEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusAllEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusLazySomeEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusEagerSomeEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusSomeEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlers.KiwoomOpenApiPlusSomeBidirectionalEventHandler




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



