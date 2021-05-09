:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientSideSignalConnector`
================================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientSideSignalConnector


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusServiceClientSideSignalConnector.KiwoomOpenApiPlusServiceClientSideSignalConnector




.. class:: KiwoomOpenApiPlusServiceClientSideSignalConnector(stub, name)


   .. attribute:: _lock
      

      

   .. attribute:: _observers
      

      

   .. attribute:: _max_workers
      

      

   .. attribute:: _executor
      

      

   .. method:: _stop_observer(cls, observer)
      :classmethod:


   .. method:: _get_observer(self, callback, default=None)


   .. method:: _remove_observer(self, callback)


   .. method:: _add_observer(self, callback)


   .. method:: shutdown(cls)
      :classmethod:


   .. method:: connect(self, callback)


   .. method:: disconnect(self, callback)



