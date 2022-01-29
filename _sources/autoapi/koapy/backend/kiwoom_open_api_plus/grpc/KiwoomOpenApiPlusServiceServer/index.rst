:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer`
================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer.KiwoomOpenApiPlusServiceServer




.. py:class:: KiwoomOpenApiPlusServiceServer(control, host=None, port=None, credentials=None, **kwargs)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: reinitialize_server(self)


   .. py:method:: get_host(self)


   .. py:method:: get_port(self)


   .. py:method:: start(self)


   .. py:method:: wait_for_termination(self, timeout=None)


   .. py:method:: is_running(self)


   .. py:method:: stop(self, grace=None)



