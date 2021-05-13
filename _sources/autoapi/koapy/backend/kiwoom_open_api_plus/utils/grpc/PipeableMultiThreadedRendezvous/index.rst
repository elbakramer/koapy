:mod:`koapy.backend.kiwoom_open_api_plus.utils.grpc.PipeableMultiThreadedRendezvous`
====================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.grpc.PipeableMultiThreadedRendezvous


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.grpc.PipeableMultiThreadedRendezvous.PipeableMultiThreadedRendezvous




.. class:: PipeableMultiThreadedRendezvous(rendezvous, iterator=None)


   Bases: :py:obj:`collections.abc.Iterator`

   .. method:: __next__(self)

      Return the next item from the iterator. When exhausted, raise StopIteration


   .. method:: pipe(self, func)


   .. method:: __getattr__(self, name)



