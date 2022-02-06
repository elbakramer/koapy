:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusConditionEventHandler`
==============================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusConditionEventHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusConditionEventHandler.KiwoomOpenApiPlusConditionEventHandler




.. py:class:: KiwoomOpenApiPlusConditionEventHandler(control, request, context, screen_manager)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)


   .. py:method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, _datalength, _errorcode, _message, _splmmsg)



