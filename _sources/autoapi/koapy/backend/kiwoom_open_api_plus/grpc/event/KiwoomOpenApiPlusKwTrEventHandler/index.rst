:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusKwTrEventHandler`
=========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusKwTrEventHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusKwTrEventHandler.KiwoomOpenApiPlusKwTrEventHandler




.. py:class:: KiwoomOpenApiPlusKwTrEventHandler(control, request, context, screen_manager)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)


   .. py:method:: OnEventConnect(self, errcode)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)



