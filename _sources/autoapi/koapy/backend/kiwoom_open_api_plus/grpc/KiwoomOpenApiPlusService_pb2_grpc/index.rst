:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusService_pb2_grpc`
================================================================================

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



.. class:: KiwoomOpenApiPlusServiceStub(channel)


   Bases: :py:obj:`object`

   Missing associated documentation comment in .proto file.


.. class:: KiwoomOpenApiPlusServiceServicer

   Bases: :py:obj:`object`

   Missing associated documentation comment in .proto file.

   .. method:: Call(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: Listen(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: BidirectionalListen(self, request_iterator, context)

      Missing associated documentation comment in .proto file.


   .. method:: CustomListen(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: CustomCallAndListen(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: LoginCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: TransactionCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: OrderCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: RealCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: LoadConditionCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: ConditionCall(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: BidirectionalRealCall(self, request_iterator, context)

      Missing associated documentation comment in .proto file.


   .. method:: OrderListen(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: SetLogLevel(self, request, context)

      Missing associated documentation comment in .proto file.



.. function:: add_KiwoomOpenApiPlusServiceServicer_to_server(servicer, server)


.. class:: KiwoomOpenApiPlusService

   Bases: :py:obj:`object`

   Missing associated documentation comment in .proto file.

   .. method:: Call(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: Listen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: BidirectionalListen(request_iterator, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: CustomListen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: CustomCallAndListen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: LoginCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: TransactionCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: OrderCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: RealCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: LoadConditionCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: ConditionCall(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: BidirectionalRealCall(request_iterator, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: OrderListen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. method:: SetLogLevel(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:



