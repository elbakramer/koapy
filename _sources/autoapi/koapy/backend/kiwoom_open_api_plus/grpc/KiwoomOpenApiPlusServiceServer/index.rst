:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer`
=============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceServer.KiwoomOpenApiPlusServiceServer




.. class:: KiwoomOpenApiPlusServiceServer(control, host=None, port=None, max_workers=None)


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: __del__(self)


   .. method:: reinitialize_server(self)


   .. method:: get_host(self)


   .. method:: get_port(self)


   .. method:: start(self)


   .. method:: wait_for_termination(self, timeout=None)


   .. method:: is_running(self)


   .. method:: stop(self, grace=None)


   .. method:: __getattr__(self, name)



