:py:mod:`koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyServiceServicer`
==============================================================================

.. py:module:: koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyServiceServicer


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyServiceServicer.CybosPlusEvent
   koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyServiceServicer.CybosPlusEventIterator
   koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyServiceServicer.CybosPlusEventHandler
   koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyServiceServicer.CybosPlusProxyServiceServicer




.. py:class:: CybosPlusEvent(iterator)

   .. py:method:: done(self)


   .. py:method:: wait_for_done(self)



.. py:class:: CybosPlusEventIterator(handler)

   .. py:method:: notify(self)



.. py:class:: CybosPlusEventHandler

   .. py:method:: OnRecieved(self)



.. py:class:: CybosPlusProxyServiceServicer

   Bases: :py:obj:`koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyService_pb2_grpc.CybosPlusProxyServiceServicer`

   Missing associated documentation comment in .proto file.

   .. py:method:: Dispatch(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: Property(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: Method(self, request, context)

      Missing associated documentation comment in .proto file.


   .. py:method:: Event(self, request_iterator, context)

      Missing associated documentation comment in .proto file.



