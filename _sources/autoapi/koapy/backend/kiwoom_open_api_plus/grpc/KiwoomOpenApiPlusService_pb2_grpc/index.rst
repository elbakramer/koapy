:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusService_pb2_grpc`
===================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusService_pb2_grpc

.. autoapi-nested-parse::

   Client and server classes corresponding to protobuf-defined services.



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusService_pb2_grpc.KiwoomOpenApiPlusServiceStub
   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusService_pb2_grpc.KiwoomOpenApiPlusServiceServicer
   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusService_pb2_grpc.KiwoomOpenApiPlusService



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusService_pb2_grpc.add_KiwoomOpenApiPlusServiceServicer_to_server



.. py:class:: KiwoomOpenApiPlusServiceStub(channel)

   Bases: :py:obj:`object`

   Missing associated documentation comment in .proto file.


.. py:class:: KiwoomOpenApiPlusServiceServicer

   Bases: :py:obj:`object`

   Missing associated documentation comment in .proto file.

   .. py:method:: Call(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: Listen(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: BidirectionalListen(self, request_iterator, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: CustomListen(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: CustomCallAndListen(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: LoginCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: TransactionCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: OrderCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: RealCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: LoadConditionCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: ConditionCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: BidirectionalRealCall(self, request_iterator, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: OrderListen(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: SetLogLevel(self, request, context)

      Missing associated documentation comment in .proto file.



.. py:function:: add_KiwoomOpenApiPlusServiceServicer_to_server(servicer, server)


.. py:class:: KiwoomOpenApiPlusService

   Bases: :py:obj:`object`

   Missing associated documentation comment in .proto file.

   .. py:method:: Call(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: Listen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: BidirectionalListen(request_iterator, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: CustomListen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: CustomCallAndListen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: LoginCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: TransactionCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: OrderCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: RealCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: LoadConditionCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: ConditionCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: BidirectionalRealCall(request_iterator, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: OrderListen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: SetLogLevel(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:



