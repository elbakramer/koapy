:mod:`koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyServiceServicer`
===========================================================================

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




.. class:: CybosPlusEvent(iterator)


   .. method:: __del__(self)


   .. method:: done(self)


   .. method:: wait_for_done(self)



.. class:: CybosPlusEventIterator(handler)


   .. method:: __del__(self)


   .. method:: notify(self)


   .. method:: __next__(self)



.. class:: CybosPlusEventHandler


   .. method:: OnRecieved(self)


   .. method:: __iter__(self)



.. class:: CybosPlusProxyServiceServicer

   Bases: :py:obj:`koapy.backend.daishin_cybos_plus.proxy.CybosPlusProxyService_pb2_grpc.CybosPlusProxyServiceServicer`

   Missing associated documentation comment in .proto file.

   .. attribute:: _lock
      

      

   .. attribute:: _dispatches
      

      

   .. attribute:: _handlers
      

      

   .. method:: _EnsureDispatch(self, prog)


   .. method:: _GetHandler(self, prog)


   .. method:: Dispatch(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: Property(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: Method(self, request, context)

      Missing associated documentation comment in .proto file.


   .. method:: Event(self, request_iterator, context)

      Missing associated documentation comment in .proto file.



