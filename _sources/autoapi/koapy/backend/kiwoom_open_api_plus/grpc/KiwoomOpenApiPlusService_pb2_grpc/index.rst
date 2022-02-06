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

      1. rpcs for general function calls

      unary rpc for an arbitrary function call,
      can invoke arbitrary function on the server side by giving its name and arguments,
      currently only simple data types like str and int are supported for arguments and return values


   .. py:method:: Listen(self, request, context)

      2. rpcs for listening and handling events

      server streaming rpc usually for listening events,
      server will simply send stream items to client whenever event that is being listened is triggered,
      client can handle those events solely on its own on client side but there is no guarantee that it will be synced with the server,
      which means that event handler on the server side will not wait for the client to finish handling each event


   .. py:method:: BidirectionalListen(self, request_iterator, context)

      bidirectional streaming rpc usually for listening and handling events with proper callbacks,
      server will send an stream item to client whenever an event is triggered and will wait for an client's ack,
      so that following callbacks from the client can actually be processed inside the server's event handler context


   .. py:method:: LoginCall(self, request, context)

      3. rpcs for simple use cases that can be categorized into serveral distinct usage patterns

      server streaming rpc for login/connect scenario,
      would invoke Connect() and wait for OnEventConnect() event to test its success


   .. py:method:: TransactionCall(self, request, context)

      server streaming rpc for general transaction requests,
      would invoke CommRqData() with several SetInputValue()s for a transaction request,
      would wait for OnReceiveTrData() events,
      would handle those events to gather results by invoking GetRepeatCnt() and GetCommData() inside,
      might do additional CommRqData() and SetInputValue() inside event handler for possible consecutive lookups


   .. py:method:: OrderCall(self, request, context)

      server streaming rpc for making orders (buy/sell + update/cancel),
      would invoke SendOrder() for submitting an order,
      would wait for OnReceiveTrData() and OnReceiveChejanData() events to track its progress


   .. py:method:: RealCall(self, request, context)

      server streaming rpc for listening realtime data events,
      certain transaction requests would also register some realtime data to be sent,
      but usually would just call SetRealReg() to register desired realtime data to listen explicitly,
      and would call SetRealRemove() to unregister them after done using,
      would wait for OnReceiveRealData() events


   .. py:method:: LoadConditionCall(self, request, context)

      server streaming rpc for loading condition settings for conditioned search,
      would call GetConditionLoad() and wait for OnReceiveConditionVer() event to test its success


   .. py:method:: ConditionCall(self, request, context)

      server streaming rpc for conditioned search (serching stocks with serveral conditions),
      would call SendCondition() and wait for OnReceiveTrCondition() or OnReceiveRealCondition() based on its requested type


   .. py:method:: BidirectionalRealCall(self, request_iterator, context)

      4. rpcs for more complex use cases based on the previously categorized simple cases above

      bidirectional streaming rpc for listening realtime data events,
      with capability of managing observation pool (what stocks, what fields to listen to) online,
      those management requests would be sent over the client streaming line,
      and ordinary realtime data events would be sent over the server streaming line


   .. py:method:: OrderListen(self, request, context)

      server streaming rpc for just listening order events (without submiting any order request compared to the simple case),
      this is one-sided streaming rpc (server streaming rpc) like Listen() rpc,
      so server would just send stream items with no consideration on coordination with its client


   .. py:method:: CustomListen(self, request, context)

      5. rpcs for customized usage scenario (when there is no proper predefined interface to utilize)

      pretty much similar to server streaming Listen() rpc,
      but event handler would be instantiated dynamically based on the code given through the request


   .. py:method:: CustomCallAndListen(self, request, context)

      pretty much similar to server streaming XXXCall() rpcs (or even Call() rpc),
      but event handler would be instantiated dynamically based on the code given through the request


   .. py:method:: SetLogLevel(self, request, context)

      6. rpcs for other mics scenarios

      would update log level of process that this grpc server lives



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


   .. py:method:: CustomListen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: CustomCallAndListen(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:


   .. py:method:: SetLogLevel(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None)
      :staticmethod:



