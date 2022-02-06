:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusRealEventHandler`
=========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusRealEventHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusRealEventHandler.KiwoomOpenApiPlusRealEventHandler
   koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusRealEventHandler.KiwoomOpenApiPlusBidirectionalRealEventHandler




.. py:class:: KiwoomOpenApiPlusRealEventHandler(control, request, context, screen_manager)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.grpc.event.KiwoomOpenApiPlusEventHandlerForGrpc.KiwoomOpenApiPlusEventHandlerForGrpc`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: on_enter(self)


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)


   .. py:method:: OnEventConnect(self, errcode)



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



