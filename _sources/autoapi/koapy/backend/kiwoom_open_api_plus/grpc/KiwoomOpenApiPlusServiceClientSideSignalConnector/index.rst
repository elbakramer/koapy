:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientSideSignalConnector`
===================================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientSideSignalConnector


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientSideSignalConnector.KiwoomOpenApiPlusServiceClientSideSignalConnector




.. py:class:: KiwoomOpenApiPlusServiceClientSideSignalConnector(stub, name)

   .. py:attribute:: _lock
      

      

   .. py:attribute:: _observers
      

      

   .. py:attribute:: _max_workers
      

      

   .. py:attribute:: _executor
      

      

   .. py:method:: _stop_observer(cls, observer)
      :classmethod:


   .. py:method:: _get_observer(self, callback, default=None)


   .. py:method:: _remove_observer(self, callback)


   .. py:method:: _add_observer(self, callback)


   .. py:method:: shutdown(cls)
      :classmethod:


   .. py:method:: connect(self, callback)


   .. py:method:: disconnect(self, callback)



