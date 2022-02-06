:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusOrderEventHandler`
==========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusOrderEventHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusOrderEventHandler.KiwoomOpenApiPlusBaseOrderEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusOrderEventHandler.KiwoomOpenApiPlusAllOrderEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusOrderEventHandler.KiwoomOpenApiPlusOrderEventHandler




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



